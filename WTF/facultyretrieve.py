import streamlit as st
import pandas as pd
from pymongo import MongoClient, ReturnDocument
from bson.objectid import ObjectId
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica", 10)  # Set font and font size for header
    pdf.drawString(30, height - 30, f"SAR DOCUMENT - {username}")  # Display username with title
    pdf.line(30, height - 35, width - 30, height - 35)
    y = height - 50

    for collection_name, df in data.items():
        pdf.drawString(30, y, f"SAR DOCUMENT - {username} - {collection_name}")
        y -= 15

        # Calculate column widths
        column_width = (width - 60) / len(df.columns)

        # Draw table headers
        for col_idx, column in enumerate(df.columns):
            pdf.drawString(30 + col_idx * column_width, y, str(column))
        y -= 15
        pdf.line(30, y, width - 30, y)
        y -= 15

        # Draw table data
        for _, row in df.iterrows():
            for col_idx, (col_name, item) in enumerate(row.items()):
                text = str(item)
                while pdf.stringWidth(text) > (column_width - 10):
                    text = text[:len(text) - 1]  # Trim text until it fits
                pdf.drawString(30 + col_idx * column_width, y, text)
            y -= 15
            if y < 40:  # Create a new page if space runs out
                pdf.showPage()
                y = height - 30
                pdf.setFont("Helvetica", 10)  # Reset font and font size for new page
                pdf.drawString(30, y, f"SAR DOCUMENT - {username}")  # Redraw general header on new page
                pdf.line(30, height - 35, width - 30, height - 35)
                y -= 50  # Adjust y position for new page
                pdf.drawString(30, y, f"SAR DOCUMENT - {username} - {collection_name}")  # Redraw specific header on new page
                y -= 15

        y -= 20  # Space after each collection

    pdf.save()
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
