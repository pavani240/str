import streamlit as st
from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l14']  # Replace 'lll03' with your actual collection name
collection_users=db['users']
def main(username):
    with st.form("l14"):
        st.title("RESEARCH GUIDANCE (Ph.D/M.Phil)")

        n1 = st.text_input("No. Of STUDENTS Completed Ph.D/M.Phil:")
        st.write("No. Of STUDENTS doing Ph.D/M.Phil in present assessment year:")
        deg = st.text_input("Degree", value="", placeholder="Enter Degree")
        uni = st.text_input("University", value="", placeholder="Enter University")
        gui = st.text_input("Guide/Co-Guide", value="", placeholder="Enter Guide/Co-Guide")
        frod3 = st.date_input(
            "Date of Registration",
            (datetime.datetime.now().date()),
            format="MM.DD.YYYY",
        )
        stype = st.text_input("Student Particulars", value="", placeholder="Enter Particulars Of Student")

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (n1 and deg and uni and gui and stype):
                st.error("Please fill out all required fields.")
                return
            
            try:
                # Convert date to datetime.datetime
                frod3 = datetime.datetime.combine(frod3, datetime.datetime.min.time())
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
                    "students_completed": n1,
                    "degree": deg,
                    "university": uni,
                    "guide": gui,
                    "date_of_registration": frod3,
                    "student_particulars": stype,
                    "department": department,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
