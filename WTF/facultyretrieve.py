import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pymongo import MongoClient

# MongoDB connection details
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

def fetch_all_data(username):
    """
    Fetches data from all collections for the given username, excluding '_id' column.
    """
    data = {}
    for i in range(1, 9):
        collection_name = f"l{i}"
        collection = db[collection_name]
        result = list(collection.find({"username": username}))
        if result:
            df = pd.DataFrame(result)
            if '_id' in df.columns:
                df.drop(columns=['_id'], inplace=True)
            if 'username' in df.columns:
                df.drop(columns=['username'], inplace=True)
            data[collection_name] = df
    return data

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
    Displays table selection and handles data retrieval and PDF download flow.
    """
    st.title("Retrieval Page")

    # Display collection selection
    table = st.selectbox("Select collection/page", [f"l{i}" for i in range(1, 9)])

    # Submit button
    if st.button("Submit"):
        if table:
            # Validate collection name against allowed values
            allowed_collections = [f"l{i}" for i in range(1, 9)]
            if table in allowed_collections:
                collection = db[table]
                result = list(collection.find({"username": username}))
                if result:
                    df = pd.DataFrame(result)
                    if '_id' in df.columns:
                        df.drop(columns=['_id'], inplace=True)
                    if 'username' in df.columns:
                        df.drop(columns=['username'], inplace=True)
                    st.write(df)  # Display data in a tabular format in Streamlit

                    # Add modify button for each row if needed
                    # for i, row in df.iterrows():
                    #     if st.button(f"Modify row {i+1}", key=f"modify_{i}"):
                    #         st.session_state.modify_row = row.to_dict()
                    #         st.session_state.modify_collection = table
                    #         st.experimental_rerun()  # Trigger a rerun
                else:
                    st.write("No data found for the given username.")
            else:
                st.write("Invalid collection selected.")
        else:
            st.write("Please select a collection.")

    # Download PDF button
    if st.button("Download PDF"):
        data = fetch_all_data(username)
        if data:
            pdf_buffer = create_pdf(data, username)
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name=f"SAR_DOCUMENT_{username}.pdf",
                mime="application/pdf"
            )
        else:
            st.write("No data available to download.")

if __name__ == "__main__":
    st.title("Retrieval Page")
    if "username" not in st.session_state:
        st.session_state.username = "default_username"  # Set a default username or use a login method to get the actual username
    main(st.session_state.username)
