import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# MongoDB connection details
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
status_collection = db['status']  # Status collection for approvals and reviews
notifications_collection = db['notifications']  # Notifications collection

def retrieve_status_notifications(username):
    """
    Retrieves both status updates (approvals and reviews) and notifications for the faculty member.
    """
    # Retrieve status updates
    query_status = {"username": username}
    status_notifications = list(status_collection.find(query_status))

    # Retrieve notifications
    query_notifications = {"username": username}
    regular_notifications = list(notifications_collection.find(query_notifications))

    return status_notifications, regular_notifications

def main(username):
    st.title("Faculty Notification Page")
    
    # Retrieve notifications (status updates and regular notifications) for the faculty member
    status_notifications, regular_notifications = retrieve_status_notifications(username)
    
    if status_notifications or regular_notifications:
        if status_notifications:
            st.subheader(f"Principal Notifications for {username}:")
            for notification in status_notifications:
                
                if 'review' in notification:
                    st.write(f"- Status: {notification['status']}")
                    st.info(f"   Review: {notification['review']}")
                st.write(f"   Timestamp: {notification['timestamp']}")
                st.write("")  # Empty line for spacing
        
        if regular_notifications:
            st.subheader(f"HOD Notifications for {username}:")
            for notification in regular_notifications:
                st.info(f"- {notification['message']} (Category: {notification['category']})")
                st.write(f"   Timestamp: {notification['timestamp']}")
                st.write("")  # Empty line for spacing

    else:
        st.write("No notifications found.")

if __name__ == "__main__":
    username = "faculty_username"  # Replace with actual logged-in faculty username
    main(username)
