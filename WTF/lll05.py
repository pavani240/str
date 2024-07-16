import streamlit as st
from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['lll05']  # Replace 'lll05' with your actual collection name

def main():
    with st.form("lll5"):
        st.title("PATENTS")

        n1 = st.text_input("No. Of PATENTS Filed upto previous assessment year:")
        n2 = st.text_input("No. Of PATENTS obtained upto previous assessment year:")
        st.write("PATENTS Published in present assessment year:")
        sop = st.text_input("Status Of Patent", value="", placeholder="Enter Status Of Patent")
        dof = st.date_input("Date of Registration", (datetime.datetime.now()), format="MM.DD.YYYY")
        iss = st.text_input("Description Of Patent", value="", placeholder="Enter Description of patent")

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (n1 and n2 and sop and iss):
                st.error("Please fill out all required fields.")
                return
            
            try:
                # Convert date to datetime.datetime
                dof = datetime.datetime.combine(dof, datetime.datetime.min.time())

                data = {
                    "patents_filed_previous": n1,
                    "patents_obtained_previous": n2,
                    "status_of_patent": sop,
                    "date_of_registration": dof,
                    "description_of_patent": iss,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
