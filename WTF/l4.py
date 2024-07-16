import streamlit as st
import time
from pymongo import MongoClient
import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l4']  # Replace 'l4' with your actual collection name

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    # Display warning message for 20 seconds
    warning_message = "Before submitting, please cross check all of your information is correct and no errors, changes cannot be recognized faster!! We appreciate your careful behavior in your self-appraisal."
    with st.spinner("Read Warning Message...."):
        st.warning(warning_message, icon="⚠️")
        time.sleep(20)  # Wait for 20 seconds

    # Reset session state after 20 seconds
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

    st.title("Learning Material")

    Subject = st.text_input(
        "Material Developed for Subject",
        value="",
        placeholder="Enter Your Subject"
    )

    year = st.text_input(
        "Year",
        value="",
        placeholder="Enter the Year"
    )

    dep = st.text_input(
        "Department",
        value="",
        placeholder="Department Name"
    )

    option1 = st.selectbox(
        "Type of Involvement",
        ("Single", "More than one"),
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
    )

    typem = st.text_input(
        "Type of Material Developed",
        value="",
        placeholder="Enter the Material Name"
    )

    if st.button("Submit"):
        # Check for empty fields
        if not (Subject and year and dep and typem):
            st.error("Please fill out all fields.")
            return

        try:
            data = {
                "username": username,
                "subject": Subject,
                "year": year,
                "department": dep,
                "type_of_involvement": option1,
                "type_of_material": typem,
                "date":datetime.datetime.now()
            }
            collection.insert_one(data)
            st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # You need to set the username in session state before running the main function
    st.session_state.username = "your_username"  # Replace 'your_username' with the actual username
    main(st.session_state.username)
