import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
notifications_collection = db['notifications']  # Notifications collection

def retrieve_notifications(username):
    query = {"username": username}
    notifications = list(notifications_collection.find(query))
    return notifications

def main(username):
    st.title("Faculty Notification Page")
    
    # Retrieve notifications for the faculty member
    notifications = retrieve_notifications(username)
    
    if notifications:
        st.subheader(f"Notifications for {username}:")
        for notification in notifications:
            st.info(f"- {notification['message']} (Category: {notification['category']})")
            st.write(f"   Timestamp: {notification['timestamp']}")
            st.write("")  # Empty line for spacing
    else:
        st.write("No notifications found.")

if __name__ == "__main__":
    username = "faculty_username"  # Replace with actual logged-in faculty username
    main(username)
