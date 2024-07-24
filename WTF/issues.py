import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
issues_collection = db['issues']

def submit_issue(username, issue):
    issue_entry = {
        'username': username,
        'datetime': datetime.now(),
        'issue': issue
    }
    issues_collection.insert_one(issue_entry)

def main(username):
    st.title("Submit an Issue")
    
    st.write(f"**Username:** {username}")
    st.write(f"**Date and Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    issue = st.text_area("Describe your issue:")
    
    if st.button("Submit"):
        if issue:
            submit_issue(username, issue)
            st.success("Issue submitted successfully!")
        else:
            st.error("Please enter a description of your issue.")
            
if __name__ == "__main__":
    if "username" not in st.session_state:
        st.session_state.username = "logged_in_user"  # Replace this with actual logged-in user's username
    main(st.session_state.username)