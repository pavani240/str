import streamlit as st
from pymongo import MongoClient
import datetime
import base64

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l12']  # Replace 'lll01' with your actual collection name
collection_users = db['users']

def calculate_points(journal_type, authorship_position):
    points_dict = {
        "SCI or equivalent": {"1st author": 100, "other": 20},
        "UGC referred Journals": {"1st author": 90, "other": 20},
        "Other International Journals": {"1st author": 80, "other": 10},
        "Other National Journals": {"1st author": 70, "other": 10}
    }
    return points_dict.get(journal_type, {}).get(authorship_position, 0)

def main(username):
    with st.form("l12"):
        st.title("No. Of JOURNAL PUBLICATIONS in present assessment year:")

        st.write("Journal Publication Details")
        ath = st.text_input("No of authors", value="", placeholder="Enter Number of Authors")
        pat = st.text_input("Position of authorship", value="", placeholder="Enter Position of Authorship")
        pubd = st.text_input("Publication details", value="", placeholder="Enter Publication Details")
        Jtype = st.selectbox("Journal type", [
            "", "SCI or equivalent", "UGC referred Journals", 
            "Other International Journals", "Other National Journals"
        ])

        # File uploader for PDF after journal type
        pdf_uploader1 = st.file_uploader("Upload your journal publication work in PDF", type=["pdf"], key="pdf1")

        st.write("Have you delivered any guest or expert LECTURE?")
        Subject11 = st.text_input("Host institution details", value="", placeholder="Enter Host Institution Details")
        Subject13 = st.text_input("Who are the audience", value="", placeholder="Enter Audience Details")
        Subject21 = st.text_input("Type of delivery", value="", placeholder="Enter Type of Delivery")

        # File uploader for PDF at the end
        pdf_uploader2 = st.file_uploader("Upload your lecture work in PDF", type=["pdf"], key="pdf2")

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (ath and pat and pubd and Jtype and Subject11 and Subject13 and Subject21):
                st.error("Please fill out all required fields.")
                return

            if not pdf_uploader1 or not pdf_uploader2:
                st.error("Please upload both PDFs.")
                return
            
            try:
                username = st.session_state.username  # Replace with your actual way of getting username

                # Query users collection to get department for the specified username
                user_data = collection_users.find_one({"username": username})
                if user_data:
                    department = user_data.get("department", "")
                else:
                    st.error("Username not found in users collection.")
                    return
                
                # Read the file content and encode it in base64
                pdf_content1 = pdf_uploader1.read()
                encoded_pdf1 = base64.b64encode(pdf_content1).decode('utf-8')

                pdf_content2 = pdf_uploader2.read()
                encoded_pdf2 = base64.b64encode(pdf_content2).decode('utf-8')

                # Calculate points
                points = calculate_points(Jtype, "1st author" if pat.lower() == "1st" else "other")

                data = {
                    "username": username,
                    "number_of_authors": ath,
                    "position_of_authorship": pat,
                    "publication_details": pubd,
                    "journal_type": Jtype,
                    "journal_pdf": encoded_pdf1,
                    "host_institution_details": Subject11,
                    "audience_details": Subject13,
                    "guest_lecture_delivery_type": Subject21,
                    "lecture_pdf": encoded_pdf2,
                    "department": department,
                    "points": points,
                    "date": datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success(f"Data inserted successfully! Total Points: {points}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main(st.session_state.username)
