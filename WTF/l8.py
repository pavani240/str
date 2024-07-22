import streamlit as st
import datetime
from pymongo import MongoClient
import base64

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l8']  # Replace 'l8' with your actual collection name
collection_users = db['users']  # Replace 'users' with your actual collection name for users

# Define points for various roles
points_dict = {
    "College level (Principal)": 100,
    "College level (Dean & Assoc. Dean)": 90,
    "Department level (HODs, College level section Incharges)": 80,
    "Department level Incharges & College level Committee Coordinators": 50,
    "BoS Incharge": 50,
    "Library Incharge": 50,
    "Project Co-Ordinator": 50,
    "CURRENTLY engaged Committee Memberships": 10
}

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    today = datetime.datetime.now()

    with st.form("l8"):
        st.title("Professional Roles")
        
        # College level roles
        st.write("**College level (Principal, Vice Principal, Deans etc)**")
        college_roles = []
        for i in range(2):  # Assuming 2 roles
            college_role_nature_of_work = st.text_input(f"Nature of work (College role {i+1})", value="", placeholder="Enter Nature of Work", key=f"college_role_nature_of_work_{i}")
            college_role_since = st.date_input(f"SINCE DATE (College role {i+1})", today, format="MM/DD/YYYY", key=f"college_role_since_{i}")
            college_roles.append({
                "nature_of_work": college_role_nature_of_work,
                "since_date": college_role_since.strftime("%Y-%m"),  # Extracting year and month
                "points": points_dict.get(college_role_nature_of_work, 0)
            })
        
        # Department level roles
        st.write("**Department level (HODs, College level section Incharges)**")
        departments = []
        for i in range(2):  # Assuming 2 departments
            department_name = st.text_input(f"Department {i+1}", value="", placeholder="Enter Department", key=f"department_name_{i}")
            department_nature_of_work = st.text_input(f"Nature of work (Department {i+1})", value="", placeholder="Enter Nature of Work", key=f"department_nature_of_work_{i}")
            department_since = st.date_input(f"SINCE DATE (Department {i+1})", today, format="MM/DD/YYYY", key=f"department_since_{i}")
            departments.append({
                "department": department_name,
                "nature_of_work": department_nature_of_work,
                "since_date": department_since.strftime("%Y-%m"),  # Extracting year and month
                "points": points_dict.get(department_nature_of_work, 0)
            })
        
        # Department level Incharges & Committee Coordinators
        st.write("**Department level Incharges & College level Committee Coordinators**")
        incharge_roles = ["BoS Incharge", "Library Incharge", "Project Co-Ordinator"]
        incharges = []
        for incharge in incharge_roles:
            incharge_since = st.date_input(f"SINCE DATE ({incharge})", today, format="MM/DD/YYYY", key=f"incharge_since_{incharge}")
            incharges.append({
                "nature_of_work": incharge,
                "since_date": incharge_since.strftime("%Y-%m"),  # Extracting year and month
                "points": points_dict[incharge]
            })
        
        # CURRENTLY engaged Committee Memberships
        st.write("**CURRENTLY engaged Committee Memberships**")
        memberships = []
        for i in range(4):  # Assuming 4 memberships
            membership_nature_of_work = st.text_input(f"Nature of work (Membership {i+1})", value="", placeholder="Enter Nature of Work", key=f"membership_nature_of_work_{i}")
            membership_since = st.date_input(f"SINCE DATE (Membership {i+1})", today, format="MM/DD/YYYY", key=f"membership_since_{i}")
            memberships.append({
                "nature_of_work": membership_nature_of_work,
                "since_date": membership_since.strftime("%Y-%m"),  # Extracting year and month
                "points": points_dict.get(membership_nature_of_work, 10)  # Default 10 points
            })

        # File uploader for certificates
        certificate_file = st.file_uploader("Upload your all role certificate PDF", type=["pdf"])

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if all(not role['nature_of_work'] for role in college_roles + departments + incharges + memberships):
                st.error("Please fill out at least one required field.")
                return

            if not certificate_file:
                st.error("Please upload your certificate PDF.")
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
                certificate_content = certificate_file.read()
                encoded_certificate = base64.b64encode(certificate_content).decode('utf-8')

                # Calculate total points
                total_points = sum(role['points'] for role in college_roles + departments + incharges + memberships)

                data = {
                    "username": username,
                    "college_roles": college_roles,
                    "departments": departments,
                    "incharges": incharges,
                    "memberships": memberships,
                    "department": department,
                    "certificate_file": encoded_certificate,
                    "total_points": total_points,  # Add total points to the data
                    "date": datetime.datetime.now()
                }
                
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":  # Replace 'your_username' with the actual username
    main(st.session_state.username)
