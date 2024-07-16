import streamlit as st
import time
from pymongo import MongoClient
import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l5']  # Replace 'l5' with your actual collection name

def main():
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
    
    # Display warning message for 20 seconds
    warning_message = "Before submitting, please cross check all of your information is correct and no errors, changes cannot be recognized faster!! We appreciate your careful behavior in your self-appraisal."
    with st.spinner("Read Warning Message...."):
        st.warning(warning_message, icon="⚠️")
        time.sleep(20)  # Wait for 20 seconds
    
    with st.form("l5"):   
        st.title("Certificate Courses Done")
        Subject = st.text_input("Certificate Name & Offered By", value="", placeholder="Certificate Name")
        
        option1 = st.selectbox(
            "Is the Subject relevant to your field",
            ("Yes", "No"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
        
        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not Subject:
                st.error("Please fill out the certificate name.")
                return

            try:
                data = {
                    "certificate_name": Subject,
                    "relevance": option1,
                    "date":datetime.datetime.now()
                    
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
