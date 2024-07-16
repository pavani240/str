# sent_page.py

import streamlit as st
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

def main():
    st.title("Sent Page")
    faculty_username = st.text_input("Enter Faculty Username")
    hod_feedback = st.text_area("Enter HOD Feedback", height=100)

    if st.button("Submit"):
        if faculty_username and hod_feedback:
            insert_forwarded(faculty_username, hod_feedback)
        else:
            st.warning("Please enter both Faculty Username and HOD Feedback.")

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
