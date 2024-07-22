import streamlit as st
from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l17']  # Replace 'l17' with your actual collection name
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
    with st.form("l17"):
        st.title("PRODUCT DESIGN / SOFTWARE DEVELOPMENT")

        n1 = st.text_input("No. Of Products designed/developed upto previous assessment year:")
        
        st.write("No. Of Products designed/developed upto present assessment year:")
        nop = st.text_input("Name of Product / SW", value="", placeholder="Enter Name of Product / SW")
        
        nof = st.text_input("No. Of Faculty in the team work", value="", placeholder="Enter No. Of Faculty in the team work")
        
        # Dropdown for position in the team
        pos = st.selectbox("Position in the team", options=["Single", "First or Principle person", "Other Persons"])
        pos_points = calculate_points(pos)
        
        dop = st.text_input("Description of the product / SW", value="", placeholder="Enter Description of the product / SW")

        # Display points
        st.write(f"Points for Position in Team: {pos} - {pos_points}")

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (n1 and nop and nof and dop):
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
                    "products_previous": n1,
                    "product_name": nop,
                    "faculty_count": nof,
                    "position_in_team": pos,
                    "position_points": pos_points,
                    "product_description": dop,
                    "department": department,
                    "date": datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main(st.session_state.username)
