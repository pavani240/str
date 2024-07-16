import streamlit as st
import datetime
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['ll5']  # Replace 'll5' with your actual collection name

def main():
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
    
    today = datetime.datetime.now()
    
    with st.form("ll5"):
        st.title("MEMBERSHIPS WITH PROFESSIONAL BODIES")
        
        Subject = st.text_input("Professional Body", value="", placeholder="Enter Professional Body Name")
        frod3 = st.date_input(
            "Since Date",
            today,
            format="MM.DD.YYYY",
        )
        Subject3 = st.text_input("National/International", value="", placeholder="Enter National/International")
        
        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not Subject or not frod3 or not Subject3:
                st.error("Please fill out all required fields.")
                return
            
            try:
                data = {
                    "professional_body": Subject,
                    "since_date": frod3.strftime("%Y-%m-%d"),
                    "national_or_international": Subject3,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
