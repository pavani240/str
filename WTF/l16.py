import streamlit as st
from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l16']  # Replace 'l16' with your actual collection name
collection_users = db['users']

# Define points for each patent type
PATENT_POINTS = {
    "Obtained": {
        "International": 100,
        "National": 80,
        "State": 60,
        "Local": 40
    },
    "Filed": {
        "International": 80,
        "National": 60,
        "State": 40,
        "Local": 20
    }
}

def calculate_points(patent_type, patent_category):
    return PATENT_POINTS[patent_type].get(patent_category, 0)

def main(username):
    with st.form("l16"):
        st.title("PATENTS")

        n1 = st.text_input("No. Of PATENTS Filed upto previous assessment year:")
        n2 = st.text_input("No. Of PATENTS obtained upto previous assessment year:")
        
        st.write("PATENTS Published in present assessment year:")
        sop = st.text_input("Status Of Patent", value="", placeholder="Enter Status Of Patent")
        dof = st.date_input("Date of Registration", (datetime.datetime.now()), format="MM.DD.YYYY")
        iss = st.text_input("Description Of Patent", value="", placeholder="Enter Description of patent")

        # Dropdown for patent filed
        filed_type = st.selectbox("Patent Filed Type", options=["International", "National", "State", "Local"])
        filed_points = calculate_points("Filed", filed_type)

        # Dropdown for patent obtained
        obtained_type = st.selectbox("Patent Obtained Type", options=["International", "National", "State", "Local"])
        obtained_points = calculate_points("Obtained", obtained_type)

        # Display points


        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (n1 and n2 and sop and iss):
                st.error("Please fill out all required fields.")
                return
            
            try:
                # Convert date to datetime.datetime
                dof = datetime.datetime.combine(dof, datetime.datetime.min.time())
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
                    "patents_filed_previous": n1,
                    "patents_obtained_previous": n2,
                    "status_of_patent": sop,
                    "date_of_registration": dof,
                    "description_of_patent": iss,
                    "department": department,
                    "filed_type": filed_type,
                    "filed_points": filed_points,
                    "obtained_type": obtained_type,
                    "obtained_points": obtained_points,
                    "date": datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main(st.session_state.username)
