import streamlit as st
from pymongo import MongoClient
import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['ll4']  # Replace 'll4' with your actual collection name

def main():
    with st.form("ll4"):
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
                data = {
                    "year_department": Subject,
                    "student_regd_nos": Subject3,
                    "number_of_students": Subject1,
                    "specific_remarks": Subject4,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
