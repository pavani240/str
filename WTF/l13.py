import streamlit as st
from pymongo import MongoClient
import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l13']  # Replace 'lll02' with your actual collection name
collection_users=db['users']
def main(username):
    with st.form("l13"):
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
                    "number_of_authors": ath,
                    "position_of_authorship": pat,
                    "conference_venue": pven,
                    "venue_location": Jtype,
                    "proceedings_type": ptype,
                    "department":department,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
