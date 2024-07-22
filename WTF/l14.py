import streamlit as st
from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l14']  # Replace 'lll03' with your actual collection name
collection_users = db['users']

def calculate_guidance_points(guide_type, date_of_registration):
    current_date = datetime.datetime.now()
    duration = (current_date - date_of_registration).days / 365.25  # Convert duration to years

    if guide_type.lower() == "guide":
        if duration <= 1:
            return 100
        elif 1 < duration <= 2:
            return 75
        elif 2 < duration <= 3:
            return 50
        else:
            return 25
    elif guide_type.lower() == "co-guide":
        if duration <= 1:
            return 50
        elif 1 < duration <= 2:
            return 35
        elif 2 < duration <= 3:
            return 20
        else:
            return 0
    return 0

def main(username):
    with st.form("l14"):
        st.title("RESEARCH GUIDANCE (Ph.D/M.Phil)")

        n1 = st.text_input("No. Of STUDENTS Completed Ph.D/M.Phil:")
        st.write("No. Of STUDENTS doing Ph.D/M.Phil in present assessment year:")
        deg = st.text_input("Degree", value="", placeholder="Enter Degree")
        uni = st.text_input("University", value="", placeholder="Enter University")
        gui = st.selectbox("Guide/Co-Guide", ["", "Guide", "Co-Guide"])
        frod3 = st.date_input("Date of Registration", datetime.datetime.now().date(), format="YYYY-MM-DD")
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
                
                # Calculate points
                points = calculate_guidance_points(gui, frod3)

                data = {
                    "username": username,
                    "students_completed": n1,
                    "degree": deg,
                    "university": uni,
                    "guide": gui,
                    "date_of_registration": frod3,
                    "student_particulars": stype,
                    "department": department,
                    "points": points,
                    "date": datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success(f"Data inserted successfully! Total Points: {points}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main(st.session_state.username)
