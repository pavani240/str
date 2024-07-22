import streamlit as st
from pymongo import MongoClient
import datetime
import base64

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l11']  # Replace 'll6' with your actual collection name
collection_users = db['users']  # Replace 'users' with your actual collection name for users

def calculate_points(event_type):
    points_dict = {
        "Chaired or Co-chaired (International)": 100,
        "Chaired or Co-chaired (National)": 80,
        "Delivering talks & Lectures (International)": 90,
        "Delivering talks & Lectures (National IIT/NIT Level)": 70,
        "Delivering talks & Lectures (University Level)": 50,
        "Delivering talks & Lectures (College Level)": 40
    }
    return points_dict.get(event_type, 0)

def main(username):
    with st.form("l11"):
        st.title("Chairing Sessions & Delivering Talks and Lectures")

        st.write("No. Of Chairing sessions and delivering talks & lectures up to previous assessment year:")
        lec = st.text_input("Lectures", value="", placeholder="Enter Lectures")
        dtalk = st.text_input("Delivering Talks", value="", placeholder="Enter Delivering Talks")
        ctalks = st.text_input("Chairing Talks", value="", placeholder="Enter Chairing Talks")

        st.write("No. Of Chairing sessions and delivering talks & lectures in present assessment year:")
        Subject = st.selectbox("Geographical Level of platform of delivery", [
            "", "Chaired or Co-chaired (International)", "Chaired or Co-chaired (National)", 
            "Delivering talks & Lectures (International)", "Delivering talks & Lectures (National IIT/NIT Level)", 
            "Delivering talks & Lectures (University Level)", "Delivering talks & Lectures (College Level)"
        ])
        Subject3 = st.text_input("Inside or out campus", value="", placeholder="Enter Inside or Out Campus")
        Subject1 = st.text_input("Name of the platform", value="", placeholder="Enter Platform Name")
        Subject4 = st.text_input("Type of delivery", value="", placeholder="Enter Type of Delivery")

        st.write("Have you delivered any guest or expert LECTURE?")
        Subject11 = st.text_input("Host institution details", value="", placeholder="Enter Host Institution Details")
        Subject13 = st.text_input("Who are the audience", value="", placeholder="Enter Audience Details")
        Subject21 = st.text_input("Type of guest or expert lecture delivered", value="", placeholder="Enter Type of Delivery")

        # File uploader for PDF
        file_uploader = st.file_uploader("Upload your all work in PDF", type=["pdf"])

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Check for empty fields
            if not (lec and dtalk and ctalks and Subject and Subject3 and Subject1 and Subject4 and Subject11 and Subject13 and Subject21):
                st.error("Please fill out all required fields.")
                return

            if not file_uploader:
                st.error("Please upload your PDF.")
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
                
                # Read the file content and encode it in base64
                pdf_content = file_uploader.read()
                encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

                points = calculate_points(Subject)

                data = {
                    "username": username,
                    "lectures": lec,
                    "delivering_talks": dtalk,
                    "chairing_talks": ctalks,
                    "geographical_level": Subject,
                    "inside_or_out_campus": Subject3,
                    "platform_name": Subject1,
                    "delivery_type": Subject4,
                    "host_institution_details": Subject11,
                    "audience_details": Subject13,
                    "guest_lecture_delivery_type": Subject21,
                    "certificate_pdf": encoded_pdf,
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
