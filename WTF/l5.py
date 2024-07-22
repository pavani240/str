import streamlit as st
import datetime
from pymongo import MongoClient
import base64

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l5']  # Replace 'l5' with your actual collection name
collection_users = db['users']  # Replace 'users' with your actual collection name for users

def get_points(certificate_type, relevance):
    """
    Function to get the points based on the type of certificate and relevance to the field of specialization.
    """
    if certificate_type == "Certificate course/Online certificate/MOOCs course offered by Foreign Universities":
        return 100 if relevance == "Yes" else 50
    elif certificate_type == "Certificate course/Online certificate/MOOCs course offered by IIT/NIT":
        return 75 if relevance == "Yes" else 35
    elif certificate_type == "Certificate course/Online certificate/MOOCs course offered by lower than IIT/NIT institutes or universities":
        return 50 if relevance == "Yes" else 25
    return 0

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    with st.form("l5"):
        st.title("Certificate Courses Done")

        certificate_options = [
            "Certificate course/Online certificate/MOOCs course offered by Foreign Universities",
            "Certificate course/Online certificate/MOOCs course offered by IIT/NIT",
            "Certificate course/Online certificate/MOOCs course offered by lower than IIT/NIT institutes or universities"
        ]
        
        certificate_type = st.selectbox(
            "Type of Certificate",
            options=certificate_options,
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
        
        relevance = st.selectbox(
            "Is the Subject Relevant to Your Field",
            ("Yes", "No"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
        
        certificate_file = st.file_uploader("Upload Your Certificate PDF", type=["pdf"])

        # Calculate points based on selected options
        points = get_points(certificate_type, relevance)



        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not certificate_file:
                st.error("Please upload your certificate PDF.")
                return
            
            try:
                # Query users collection to get department for the specified username
                user_data = collection_users.find_one({"username": username})
                if user_data:
                    department = user_data.get("department", "")
                else:
                    st.error("Username not found in users collection.")
                    return
                
                # Read the file content and encode it in base64
                certificate_content = certificate_file.read()
                encoded_certificate = base64.b64encode(certificate_content).decode('utf-8')

                data = {
                    "username": username,
                    "certificate_type": certificate_type,
                    "relevance": relevance,
                    "points": points,  # Add points to the data
                    "department": department,
                    "date": datetime.datetime.now(),
                    "certificate_file": encoded_certificate
                }
                
                # Insert data into l5 collection
                collection.insert_one(data)
                st.success("Data inserted successfully!")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    # Ensure the username is set in session state before running the main function  # Replace 'your_username' with the actual username
    main(st.session_state.username)
