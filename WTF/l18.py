import streamlit as st
from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l18']  # Replace 'l18' with your actual collection name
collection_users = db['users']

# Define points for each position in the team
POSITION_POINTS = {
    "Single": 100,
    "First or Principle person": 50,
    "Other Persons": 10
}

def calculate_points(position):
    return POSITION_POINTS.get(position, 0)

def main(username):
    with st.form("l18"):
        st.title("CONSULTANCY")

        n1 = st.text_input("Total Consultancy upto previous assessment year: (in Rs.)")
        
        st.write("Consultancy in present assessment year:")
        toc = st.text_input("Title of Consultancy work", value="", placeholder="Enter Title of Consultancy work")
        
        nga = st.text_input("Name of Granting Agency", value="", placeholder="Name of Granting Agency")
        
        nci = st.text_input("No of Coordinators involved", value="", placeholder="Enter No of Coordinators involved")
        
        # Dropdown for position in the team
        poc = st.selectbox("Position in order of coordinatorship", options=["Single", "First or Principle person", "Other Persons"])
        poc_points = calculate_points(poc)
        
        sin = st.date_input(
            "Since:",
            (datetime.datetime.now()),
            format="MM.DD.YYYY",
        )
        
        gm = st.text_input("Grant/Amount mobilised", value="", placeholder="Enter Grant/Amount mobilised")

        # Display points

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (n1 and toc and nga and nci and gm):
                st.error("Please fill out all required fields.")
                return
            
            try:
                # Convert date to datetime.datetime
                sin = datetime.datetime.combine(sin, datetime.datetime.min.time())
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
                    "total_consultancy_previous": n1,
                    "title_consultancy_work": toc,
                    "granting_agency": nga,
                    "coordinators_involved": nci,
                    "position_coordinatorship": poc,
                    "position_points": poc_points,
                    "since_date": sin,
                    "grant_amount_mobilised": gm,
                    "department": department,
                    "date": datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main(username=None)
