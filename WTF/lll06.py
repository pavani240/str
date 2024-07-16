import streamlit as st
from pymongo import MongoClient
import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['lll06']  # Replace 'lll06' with your actual collection name

def main():
    with st.form("lll6"):
        st.title("PRODUCT DESIGN / SOFTWARE DEVELOPMENT")

        n1 = st.text_input("No. Of Products designed/developed upto previous assessment year:")
        st.write("No. Of Products designed/developed upto present assessment year:")
        nop = st.text_input("Name of Product / SW", value="", placeholder="Enter Name of Product / SW")
        nof = st.text_input("No. Of Faculty in the team work", value="", placeholder="Enter No. Of Faculty in the team work")
        pos = st.text_input("Position in the team", value="", placeholder="Enter Position in the team")
        dop = st.text_input("Description of the product / SW", value="", placeholder="Enter Description of the product / SW")

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (n1 and nop and nof and pos and dop):
                st.error("Please fill out all required fields.")
                return
            
            try:
                data = {
                    "products_previous": n1,
                    "product_name": nop,
                    "faculty_count": nof,
                    "position_in_team": pos,
                    "product_description": dop,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
