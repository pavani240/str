import streamlit as st
from pymongo import MongoClient
import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l9']  # Replace 'll4' with your actual collection name
collection_users=db['users']
def main(username):
    with st.form("l9"):
        st.title("Students Counselling/Mentoring")
        
        Subject = st.text_input("Year & Department", value="", placeholder="Enter Year & Department")
        Subject3 = st.text_input("Regd. no(s). of student", value="", placeholder="18A51A0501-18A51A0521")
        Subject1 = st.text_input("Number of students", value="", placeholder="Enter number of students")
        Subject4 = st.text_input("Specific remarks", value="", placeholder="Enter specific remarks (e.g., 16 Selected in Campus Interviews)")
        
        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not Subject or not Subject3 or not Subject1 or not Subject4:
                st.error("Please fill out all required fields.")
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
                data = {
                    "username": username,
                    "year_department": Subject,
                    "student_regd_nos": Subject3,
                    "number_of_students": Subject1,
                    "specific_remarks": Subject4,
                    "department":department,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
