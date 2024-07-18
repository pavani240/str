import streamlit as st
from pymongo import MongoClient
import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l11']  # Replace 'll6' with your actual collection name
collection_users=db['users']
def main(username):
    with st.form("l11"):
        st.title("Number Of Chairing Sessions & Delivering talks and lectures")

        st.write("No. Of Chairing sessions and delivering talks & lectures up to previous assessment year:")
        lec = st.text_input("Lectures", value="", placeholder="Enter Lectures")
        dtalk = st.text_input("Delivering Talks", value="", placeholder="Enter Delivering Talks")
        ctalks = st.text_input("Chairing Talks", value="", placeholder="Enter Chairing Talks")

        st.write("No. Of Chairing sessions and delivering talks & lectures in present assessment year:")
        Subject = st.text_input("Geographical Level of platform of delivery", value="", placeholder="Enter Geographical Level")
        Subject3 = st.text_input("Inside or out campus", value="", placeholder="Enter Inside or Out Campus")
        Subject1 = st.text_input("Name of the platform", value="", placeholder="Enter Platform Name")
        Subject4 = st.text_input("Type of delivery", value="", placeholder="Enter Type of Delivery")

        st.write("Have you delivered any guest or expert LECTURE?")
        Subject11 = st.text_input("Host institution details", value="", placeholder="Enter Host Institution Details")
        Subject13 = st.text_input("Who are the audience", value="", placeholder="Enter Audience Details")
        Subject21 = st.text_input("Type of guest or expert lecture deliveried", value="", placeholder="Enter Type of Delivery")

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (lec and dtalk and ctalks and Subject and Subject3 and Subject1 and Subject4 and Subject11 and Subject13 and Subject21):
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
                    "department":department,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
