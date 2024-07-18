import streamlit as st
from pymongo import MongoClient
import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l12']  # Replace 'lll01' with your actual collection name
collection_users=db['users']
def main(username):
    with st.form("l12"):
        st.title("No. Of JOURNAL PUBLICATIONS in present assessment year:")

        st.write("No of authors")
        ath = st.text_input("No of authors", value="", placeholder="Enter Number of Authors")
        pat = st.text_input("Position of authorship", value="", placeholder="Enter Position of Authorship")
        pubd = st.text_input("Publication details", value="", placeholder="Enter Publication Details")
        Jtype = st.text_input("Journal type", value="", placeholder="Enter Journal Type")

        st.write("Have you delivered any guest or expert LECTURE?")
        Subject11 = st.text_input("Host institution details", value="", placeholder="Enter Host Institution Details")
        Subject13 = st.text_input("Who are the audience", value="", placeholder="Enter Audience Details")
        Subject21 = st.text_input("Type of delivery", value="", placeholder="Enter Type of Delivery")

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (ath and pat and pubd and Jtype and Subject11 and Subject13 and Subject21):
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
                    "publication_details": pubd,
                    "journal_type": Jtype,
                    "host_institution_details": Subject11,
                    "audience_details": Subject13,
                    "guest_lecture_delivery_type": Subject21,
                    "department":department,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
