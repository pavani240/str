# sent_page.py

import streamlit as st
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

def main():
    # Assuming HOD username is stored in session state upon login
    if "username" not in st.session_state:
        st.error("HOD details not found in session state. Please log in.")
        return

    hod_username = st.session_state.username

    # Retrieve HOD department from the users collection
    hod_department = get_hod_department(hod_username)
    if not hod_department:
        st.error("Failed to retrieve HOD department.")
        return

    st.title("Sent Page")
    faculty_username = st.text_input("Enter Faculty Username")
    hod_feedback = st.text_area("Enter HOD Feedback", height=100)

    if st.button("Submit"):
        if faculty_username and hod_feedback:
            if validate_username(faculty_username, hod_department):
                insert_forwarded(faculty_username, hod_feedback)
        else:
            st.warning("Please enter both Faculty Username and HOD Feedback.")

def get_hod_department(hod_username):
    users_collection = db['users']
    hod_user = users_collection.find_one({"username": hod_username})
    if hod_user:
        return hod_user.get('department')
    else:
        return None

def validate_username(faculty_username, hod_department):
    users_collection = db['users']
    user = users_collection.find_one({"username": faculty_username})
    if user:
        if user['department'] == hod_department:
            return True
        else:
            st.warning("Illegal operation: User belongs to a different branch. Contact admin.")
            return False
    else:
        st.warning("No user found with the given username.")
        return False

def insert_forwarded(username, feedback):
    forwarded_collection = db['forwarded']
    forwarded_data = {
        "username": username,
        "feedback": feedback,
        "timestamp": datetime.now()
    }
    try:
        result = forwarded_collection.insert_one(forwarded_data)
        st.success("Feedback forwarded successfully.")
    except Exception as e:
        st.error(f"Error inserting forwarded data: {e}")

if __name__ == "__main__":
    main()
