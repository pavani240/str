import streamlit as st
from pymongo import MongoClient
import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['lll02']  # Replace 'lll02' with your actual collection name

def main():
    with st.form("lll02"):
        st.title("No. Of CONFERENCE PUBLICATIONS in present assessment year:")

        ath = st.text_input("No of authors", value="", placeholder="Enter Number of Authors")
        pat = st.text_input("Position of authorship", value="", placeholder="Enter Position of Authorship")
        pven = st.text_input("Venue of Conference", value="", placeholder="Enter Conference Venue")
        Jtype = st.text_input("Venue at India/Abroad", value="", placeholder="India/Abroad")
        ptype = st.text_input("Proceedings type", value="", placeholder="Enter Proceedings Type")

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (ath and pat and pven and Jtype and ptype):
                st.error("Please fill out all required fields.")
                return
            
            try:
                data = {
                    "number_of_authors": ath,
                    "position_of_authorship": pat,
                    "conference_venue": pven,
                    "venue_location": Jtype,
                    "proceedings_type": ptype,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
