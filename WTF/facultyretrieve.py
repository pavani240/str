import streamlit as st
import pandas as pd
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch  # Add this import

# MongoDB connection details
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

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

def create_pdf(data, username):
    """
    Generates a PDF file from the given data.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles["Heading1"]
    title_style.alignment = 1  # Center align the title

    header_style = ParagraphStyle(
        name='HeaderStyle',
        fontSize=8,
        textColor=colors.white,
        alignment=1,  # Center align the header text
        backColor=colors.yellow
    )

    cell_style = ParagraphStyle(
        name='CellStyle',
        fontSize=6,
        alignment=1  # Center align the cell text
    )

    elements.append(Paragraph(f"SAR DOCUMENT - {username}", title_style))

    for collection_name, df in data.items():
        elements.append(Spacer(1, 0.2 * inch))  # Add space between tables
        elements.append(Paragraph(f"{collection_name}", title_style))

        # Prepare table data with headers
        table_data = [df.columns.tolist()] + df.values.tolist()
        
        # Wrapping the header text to avoid overlap
        for i in range(len(table_data[0])):
            table_data[0][i] = Paragraph(table_data[0][i], header_style)
        
        # Adjust column widths based on the content
        col_widths = [max(len(str(cell)) for cell in col) * 0.1 * inch for col in zip(*table_data)]
        col_widths = [min(width, 1.5 * inch) for width in col_widths]  # Limit maximum width for any column

        table = Table(table_data, colWidths=col_widths)

        # Apply table styles
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.yellow),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('FONTSIZE', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ]))

        elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer

def main(username):
    """
    Main Streamlit application function.
    """
    st.title("Modify Data")

    # Fetch and display data
    data = fetch_all_data(username)
    for collection_name, df in data.items():
        st.subheader(f"Collection: {collection_name}")
        if not df.empty:
            for index, row in df.iterrows():
                st.write(f"Row {index + 1}")

                # Generate a unique key for the modify button to avoid conflicts
                modify_key = f"modify_{collection_name}_{index}"
                if st.button(f"Modify row {index + 1}", key=modify_key):
                    new_data = {}
                    for column in df.columns:
                        new_value = st.text_input(f"Enter new value for {column}", row[column], key=f"{collection_name}_{column}_{index}")
                        new_data[column] = new_value

                    # Generate a unique key for the update button to avoid conflicts
                    update_key = f"update_{collection_name}_{index}"
                    if st.button("Update", key=update_key):
                        if update_data(collection_name, str(row['_id']), new_data):
                            st.success("Data updated successfully.")
                            # Refresh data after update
                            data = fetch_all_data(username)
                        else:
                            st.error("Failed to update data.")

                else:
                    st.write(row)

        else:
            st.write(f"No data found in collection: {collection_name}")

    # Download PDF button
    if st.button("Download PDF"):
        pdf_buffer = create_pdf(data, username)
        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name=f"SAR_DOCUMENT_{username}.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    if "username" not in st.session_state:
        st.session_state.username = "default_username"  # Set a default username or use a login method to get the actual username
    main(st.session_state.username)
