import streamlit as st
import time
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
collection = db['l1']

def calpoints(option1, option2, res):
    # Logic to calculate points based on feedback and result percentage
    if option1 == "Excellent" and option2 == "Excellent":
        if int(res) >= 90:
            return 100
        elif int(res) >= 80:
            return 90
        elif int(res) >= 70:
            return 80
        else:
            return 70
    elif option1 == "Good" and option2 == "Excellent":
        if int(res) >= 90:
            return 95
        elif int(res) >= 80:
            return 85
        elif int(res) >= 70:
            return 75
        else:
            return 65
    elif option2 == "Good" and option1 == "Excellent":
        if int(res) >= 90:
            return 95
        elif int(res) >= 80:
            return 85
        elif int(res) >= 70:
            return 75
        else:
            return 65
    elif option1 == "Satisfactory" and option2 == "Excellent":
        if int(res) >= 90:
            return 90
        elif int(res) >= 80:
            return 80
        elif int(res) >= 70:
            return 70
        else:
            return 60
    elif option2 == "Satisfactory" and option1 == "Excellent":
        if int(res) >= 90:
            return 90
        elif int(res) >= 80:
            return 80
        elif int(res) >= 70:
            return 70
        else:
            return 60
    elif option1 == "Good" and option2 == "Satisfactory":
        if int(res) >= 90:
            return 85
        elif int(res) >= 80:
            return 75
        elif int(res) >= 70:
            return 65
        else:
            return 55
    elif option2 == "Good" and option1 == "Satisfactory":
        if int(res) >= 90:
            return 85
        elif int(res) >= 80:
            return 75
        elif int(res) >= 70:
            return 65
        else:
            return 55
    elif option1 == "Good" and option2 == "Good":
        if int(res) >= 90:
            return 90
        elif int(res) >= 80:
            return 80
        elif int(res) >= 70:
            return 70
        else:
            return 60
    elif option1 == "Satisfactory" and option2 == "Satisfactory":
        if int(res) >= 90:
            return 80
        elif int(res) >= 80:
            return 70
        elif int(res) >= 70:
            return 60
        else:
            return 50

def fetch_all_data(username):
    """
    Fetches data from the collection for the given username.
    """
    return list(collection.find({"username": username}))

def fetch_row_data(row_id):
    """
    Fetches a single row of data from the collection based on the row ID.
    """
    return collection.find_one({"_id": ObjectId(row_id)})

def update_data(row_id, new_data):
    """
    Updates data in the MongoDB collection.
    """
    try:
        update_result = collection.find_one_and_update(
            {"_id": ObjectId(row_id)},
            {"$set": new_data},
            return_document=True
        )
        return update_result is not None
    except Exception as e:
        st.error(f"Error updating data: {e}")
        return False

def display_form(row_data=None, row_id=None):
    """
    Displays the form with prefilled data if row_data is provided.
    """
    st.title("Theory Courses Handled")
    
    Subject = st.text_input("Subject", value=row_data["subject"] if row_data else "", placeholder="Enter Your Subject")
    dep = st.text_input("Department", value=row_data["department"] if row_data else "", placeholder="Department Name")
    section = st.text_input("Class & Section", value=row_data["section"] if row_data else "", placeholder="Enter Classname & Section || Example: 3 CSE B")
    cp = st.text_input("Classes Planned", value=row_data["classes_planned"] if row_data else "", placeholder="No. Of Classes Planned")
    ch = st.text_input("Classes Held", value=row_data["classes_held"] if row_data else "", placeholder="No. Of Classes Held")
    option1 = st.selectbox(
        "Student Feedback (Cycle 1)",
        ("Excellent", "Good", "Satisfactory"),
        index=["Excellent", "Good", "Satisfactory"].index(row_data["feedback1"]) if row_data else 0
    )
    option2 = st.selectbox(
        "Student Feedback (Cycle 2)",
        ("Excellent", "Good", "Satisfactory"),
        index=["Excellent", "Good", "Satisfactory"].index(row_data["feedback2"]) if row_data else 0
    )
    res = st.text_input("Result Of Students", value=row_data["result"] if row_data else "", placeholder="% Of Students Passed")

    if st.button("Submit"):
        # Check for empty fields
        if not (Subject and dep and section and cp and ch and res):
            st.error("Please fill out all fields.")
            return

        try:
            points = calpoints(option1, option2, res)
            new_data = {
                "username": row_data["username"] if row_data else st.session_state.username,
                "subject": Subject,
                "department": dep,
                "section": section,
                "classes_planned": cp,
                "classes_held": ch,
                "feedback1": option1,
                "feedback2": option2,
                "result": res,
                "points": points,
                "date": datetime.datetime.now()
            }
            if row_id:
                if update_data(row_id, new_data):
                    st.success("Data updated successfully!")
                else:
                    st.error("Failed to update data.")
            else:
                collection.insert_one(new_data)
                st.success("Data inserted successfully!")
        except Exception as e:
            st.error(f"An error occurred: {e}")

def main(username):
    st.title("Retrieve and Modify Data")

    # Fetch and display data
    data = fetch_all_data(username)
    
    for index, row in enumerate(data):
        st.write(f"**Row {index + 1}**")
        
        # Display data in a neat format using Markdown
        st.markdown(
            f"""
            <div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px;">
                <strong>Subject:</strong> {row['subject']}<br>
                <strong>Department:</strong> {row['department']}<br>
                <strong>Class & Section:</strong> {row['section']}<br>
                <strong>Classes Planned:</strong> {row['classes_planned']}<br>
                <strong>Classes Held:</strong> {row['classes_held']}<br>
                <strong>Feedback (Cycle 1):</strong> {row['feedback1']}<br>
                <strong>Feedback (Cycle 2):</strong> {row['feedback2']}<br>
                <strong>Result:</strong> {row['result']}<br>
                <strong>Points:</strong> {row['points']}<br>
                <strong>Date:</strong> {row['date'].strftime('%Y-%m-%d %H:%M:%S')}<br>
                <strong>Object ID:</strong> {row['_id']}<br>
            </div>
            """, unsafe_allow_html=True
        )
        modify_key = f"modify_{index}"
        if st.button(f"Modify row {index + 1}", key=modify_key):
            st.session_state.row_id = str(row['_id'])  # Store row_id in session state
            st.session_state.row_data = row      # Store row_data in session state

    if 'row_id' in st.session_state and 'row_data' in st.session_state:
        display_form(row_data=st.session_state.row_data, row_id=st.session_state.row_id)

if __name__ == "__main__":
    if "username" not in st.session_state:
        st.session_state.username = "default_username"  # Set a default username or use a login method to get the actual username
    main(st.session_state.username)
