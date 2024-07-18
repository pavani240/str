import streamlit as st
import time
from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l5']  # Replace 'l5' with your actual collection name
collection_users = db['users']  # Replace 'users' with your actual collection name for users

def main(username):
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
                # Assuming username is stored in session_state or retrieved from somewhere
                username = st.session_state.username  # Replace with your actual way of getting username
                
                # Query users collection to get department for the specified username
                user_data = collection_users.find_one({"username": username})
                if user_data:
                    department = user_data.get("department", "")
                else:
                    st.error("Username not found in users collection.")
                    return
                
                data = {
                    "username": username,
                    "certificate_name": Subject,
                    "relevance": option1,
                    "department": department,
                    "date": datetime.datetime.now()
                }
                
                # Insert data into l5 collection
                collection.insert_one(data)
                st.success("Data inserted successfully!")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
