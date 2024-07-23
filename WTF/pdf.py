import streamlit as st
import pandas as pd
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib import colors
from PyPDF2 import PdfReader, PdfWriter
import base64
from datetime import datetime

# MongoDB connection details
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
notifications_collection = db['notifications']  # Notifications collection

def fetch_all_data(username):
    """
    Fetches data from all collections for the given username, excluding '_id' and 'username' columns.
    """
    data = {}
    for i in range(1, 19):
        collection_name = f"l{i}"
        collection = db[collection_name]
        result = list(collection.find({"username": username}))
        if result:
            df = pd.DataFrame(result)
            df = df.drop(columns=['_id', 'username'])  # Drop unnecessary columns for display
            df = df.fillna('')  # Replace NaN values with empty strings
            data[collection_name] = df
    return data

def update_data(collection_name, row_id, new_data):
    """
    Updates data in MongoDB collection.
    """
    try:
        collection = db[collection_name]
        update_result = collection.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=ReturnDocument.AFTER
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False

def retrieve_notifications(username):
    """
    Retrieves notifications for the given username.
    """
    query = {"username": username}
    notifications = list(notifications_collection.find(query))
    return notifications

def calculate_row_height(text, col_width):
    """
    Calculate row height based on the length of the text.
    """
    lines = text.split('\n')
    max_lines = max(len(line) for line in lines)
    return max(0.2 * inch, max_lines * 0.2 * inch)  # Adjust multiplier as needed

def create_table_chunk(data_chunk, column_width):
    row_heights = []
    for row in data_chunk:
        max_cell_height = 0
        for cell in row:
            if isinstance(cell, str):  # Check if cell is a string
                lines = cell.split('\n')
                max_cell_height = max(max_cell_height, len(lines) * 0.2 * inch)
            else:
                max_cell_height = max(max_cell_height, 0.2 * inch)  # Default height for non-string cells
        row_heights.append(max(0.2 * inch, max_cell_height))  
    table = Table(data_chunk, colWidths=[column_width] * len(data_chunk[0]), rowHeights=row_heights)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('PADDING', (0, 0), (-1, -1), (0.1 * inch, 0.1 * inch, 0.1 * inch, 0.1 * inch)),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reduced font size
        ('WRAPON', (0, 0), (-1, -1))  # Enable text wrapping
    ]))
    return table, sum(row_heights)

def add_table_pages(df, title, pdf_writer):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=(11 * inch, 17 * inch),  # Increased page size
                            rightMargin=0.5 * inch, leftMargin=0.5 * inch, 
                            topMargin=0.5 * inch, bottomMargin=0.5 * inch, 
                            landscape=True)
    elements = []

    # Add title
    title_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),  # Reduced font size
        ('ALIGN', (0, 0), (-1, 0), 'CENTER')
    ])
    title_table = Table([[title]], colWidths=[10 * inch])  # Adjust column width for landscape
    title_table.setStyle(title_style)
    elements.append(title_table)
    elements.append(Spacer(1, 6))  # Reduced space after title

    # Calculate available space on the page
    available_space = 17 * inch - 1 * inch  # Adjust max height for landscape

    # Add tables with pagination
    num_columns = len(df.columns)
    column_width = (10 * inch) / num_columns  # Adjust column width for landscape

    # Prepare table data
    table_data = [df.columns.tolist()] + df.values.tolist()

    table_index = 0
    while table_index < len(table_data):
        chunk = table_data[table_index:table_index + 20]
        table, table_height = create_table_chunk(chunk, column_width)

        # Check if the table fits on the current page
        if table_height > available_space:
            # Start a new page
            doc.build(elements)
            pdf_buffer.seek(0)
            pdf_reader = PdfReader(pdf_buffer)
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            # Reset available space and elements
            available_space = 17 * inch - 1 * inch  # Reset space for new page
            elements = [title_table, Spacer(1, 6)]  # Re-add title for new page

        elements.append(table)
        elements.append(Spacer(1, 6))  # Reduced space after table chunk
        available_space -= table_height
        table_index += 20  # Move to the next chunk of rows

        # Check if there's enough space left on the current page
        if available_space < 0.2 * inch:  # Leave some space for the next table
            # Start a new page
            doc.build(elements)
            pdf_buffer.seek(0)
            pdf_reader = PdfReader(pdf_buffer)
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            # Reset available space and elements
            available_space = 17 * inch - 1 * inch  # Reset space for new page
            elements = [title_table, Spacer(1, 6)]  # Re-add title for new page

    # Build the final page
    if elements:
        doc.build(elements)
        pdf_buffer.seek(0)
        pdf_reader = PdfReader(pdf_buffer)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)


def create_pdf(data, notifications, username):
    """
    Generates a PDF file from the given data and notifications, and appends proofs of work.
    """
    buffer = BytesIO()
    pdf_writer = PdfWriter()

    # Add data from collections
    for collection_name, df in data.items():
        title = f"SAR DOCUMENT - {username} - {collection_name}"
        add_table_pages(df, title, pdf_writer)

    # Add notifications page
    notifications_content = f"Notifications for {username}\n\n"
    for notification in notifications:
        notifications_content += f"Message: {notification['message']}\n"
        notifications_content += f"Category: {notification['category']}\n"
        notifications_content += f"Timestamp: {notification['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=(11 * inch, 17 * inch),  # Increased page size
                             rightMargin=0.5 * inch, leftMargin=0.5 * inch, 
topMargin=0.5 * inch, bottomMargin=0.5 * inch)
    elements = []

    # Add notifications title
    title_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER')
    ])
    title_table = Table([['Notifications']], colWidths=[10 * inch])  # Adjust column width for landscape
    title_table.setStyle(title_style)
    elements.append(title_table)
    elements.append(Spacer(1, 12))  # Add space after title

    # Add notifications content
    notifications_table = Table([[notifications_content]], colWidths=[10 * inch])
    elements.append(notifications_table)

    # Build the PDF
    doc.build(elements)
    pdf_buffer.seek(0)
    pdf_reader = PdfReader(pdf_buffer)
    if pdf_buffer.getvalue():  # Check if the buffer has content
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
    else:
        print("Warning: The PDF buffer is empty after building.")

    # Add proofs of work submitted
    for collection_name in data.keys():
        collection = db[collection_name]
        for record in collection.find({"username": username}):
            proof_file_base64 = record.get("proof_file")
            if proof_file_base64:
                # Decode the base64 string
                proof_file_data = base64.b64decode(proof_file_base64)
                proof_file_buffer = BytesIO(proof_file_data)
                proof_pdf = PdfReader(proof_file_buffer)
                for page in proof_pdf.pages:
                    pdf_writer.add_page(page)

    # Save the final PDF
    with open(f"{username}_details.pdf", "wb") as f:
        pdf_writer.write(f)

    return base64.b64encode(open(f"{username}_details.pdf", "rb").read()).decode()

def main():
    st.title("Generate PDF")

    username = st.text_input("Enter Username")

    if st.button("Generate PDF") and username:
        data = fetch_all_data(username)
        notifications = retrieve_notifications(username)
        pdf_buffer = create_pdf(data, notifications, username)

        if pdf_buffer:
            st.download_button(
                label="Download PDF",
                data=base64.b64decode(pdf_buffer),
                file_name=f"{username}_details.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Error generating PDF.")

if __name__ == "__main__":
    main()