import streamlit as st
import datetime
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l10']  # Replace 'll5' with your actual collection name
collection_users=db['users']
def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
    
    today = datetime.datetime.now()
    
    with st.form("l10"):
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
                    "professional_body": Subject,
                    "since_date": frod3.strftime("%Y-%m-%d"),
                    "national_or_international": Subject3,
                    "department":department,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
