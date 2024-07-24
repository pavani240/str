# hod_page.py
import streamlit as st
import pandas as pd
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PyPDF2 import PdfReader, PdfWriter
import base64

# MongoDB connection details
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
notifications_collection = db['notifications']  # Notifications collection

def fetch_all_data(username):
    """
    Fetches data from all collections for the given username, excluding '_id' and 'username' columns.
    """
    data = {}
    pdf_files = []
    for i in range(1, 19):
        collection_name = f"l{i}"
        collection = db[collection_name]
        result = list(collection.find({"username": username}))
        if result:
            df = pd.DataFrame(result)
            df = df.drop(columns=['_id', 'username'])  # Drop unnecessary columns for display
            if 'certificate_file' in df.columns:
                pdf_files.extend(df['certificate_file'].dropna().tolist())
            data[collection_name] = df
    return data, pdf_files

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

def create_pdf(data, notifications, pdf_files, username):
    """
    Generates a PDF file from the given data and notifications.
    """
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    margin = 0.5 * inch
    usable_width = width - 2 * margin
    usable_height = height - 2 * margin

    pdf.translate(margin, margin)
    pdf.setFont("Helvetica", 8)  # Set font and font size for content
    pdf.drawString(0, usable_height, f"SAR DOCUMENT - {username}")  # Display username with title
    pdf.line(0, usable_height - 10, usable_width, usable_height - 10)

    y = usable_height - 30
    for collection_name, df in data.items():
        pdf.drawString(0, y, f"SAR DOCUMENT - {username} - {collection_name}")
        y -= 15

        # Calculate column widths
        column_widths = {col: max(pdf.stringWidth(col, "Helvetica", 8), 50) for col in df.columns}
        for _, row in df.iterrows():
            for col in df.columns:
                column_widths[col] = max(column_widths[col], pdf.stringWidth(str(row[col]), "Helvetica", 8))

        total_width = sum(column_widths.values())
        scaling_factor = usable_width / total_width if total_width > usable_width else 1.0
        column_widths = {col: width * scaling_factor for col, width in column_widths.items()}

        # Draw table headers
        for col_idx, (col, col_width) in enumerate(column_widths.items()):
            pdf.drawString(sum(list(column_widths.values())[:col_idx]), y, str(col))
        y -= 15
        pdf.line(0, y, usable_width, y)
        y -= 15

        # Draw table data
        for _, row in df.iterrows():
            for col_idx, (col, col_width) in enumerate(column_widths.items()):
                text = str(row[col])
                wrapped_text = pdf.beginText(sum(list(column_widths.values())[:col_idx]), y)
                wrapped_text.setFont("Helvetica", 8)
                wrapped_text.setTextOrigin(sum(list(column_widths.values())[:col_idx]), y)
                wrapped_text.textLines(text)
                pdf.drawText(wrapped_text)
            y -= 15
            if y < 40:  # Create a new page if space runs out
                pdf.showPage()
                pdf.translate(margin, margin)
                pdf.setFont("Helvetica", 8)  # Reset font and font size for new page
                pdf.drawString(0, usable_height, f"SAR DOCUMENT - {username}")  # Redraw general header on new page
                pdf.line(0, usable_height - 10, usable_width, usable_height - 10)
                y = usable_height - 30
                pdf.drawString(0, y, f"SAR DOCUMENT - {username} - {collection_name}")  # Redraw specific header on new page
                y -= 15
        y -= 20  # Space after each collection

    # Add notifications to the end of the PDF
    pdf.showPage()  # Start a new page for notifications
    pdf.translate(margin, margin)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(0, usable_height, f"Notifications for {username}")
    pdf.line(0, usable_height - 10, usable_width, usable_height - 10)
    y = usable_height - 30
    for notification in notifications:
        pdf.drawString(0, y, f"Message: {notification['message']}")
        y -= 15
        pdf.drawString(0, y, f"Category: {notification['category']}")
        y -= 15
        pdf.drawString(0, y, f"Timestamp: {notification['timestamp']}")
        y -= 30
        if y < 40:  # Create a new page if space runs out
            pdf.showPage()
            pdf.translate(margin, margin)
            y = usable_height - 30
    pdf.save()

    buffer.seek(0)
    output_pdf = PdfWriter()
    output_pdf.append(buffer)

    for pdf_file in pdf_files:
        pdf_data = base64.b64decode(pdf_file)
        pdf_buffer = BytesIO(pdf_data)
        pdf_reader = PdfReader(pdf_buffer)
        for page in pdf_reader.pages:
            output_pdf.add_page(page)

    output_buffer = BytesIO()
    output_pdf.write(output_buffer)
    output_buffer.seek(0)

    return output_buffer

def main():
    """
    Main Streamlit application function.
    """
    st.title("PDF VIEW")
    with st.form("download_pdf_form"):
        st.write("Enter Username to download full details as PDF:")
        username = st.text_input("Username")
        submit_button = st.form_submit_button("Download PDF")

    if submit_button:
        if username:
            data, pdf_files = fetch_all_data(username)
            notifications = retrieve_notifications(username)
            if data or notifications:
                pdf_buffer = create_pdf(data, notifications, pdf_files, username)
                st.download_button(
                    label="Download PDF",
                    data=pdf_buffer,
                    file_name=f"SAR_DOCUMENT_{username}.pdf",
                    mime="application/pdf"
                )
            else:
                st.warning(f"No data found for username: {username}")
        else:
            st.warning("Please enter a username.")

if __name__ == "__main__":
    main()
