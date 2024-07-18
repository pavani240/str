import streamlit as st
from pymongo import MongoClient
import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l15']  # Replace 'lll04' with your actual collection name
collection_users=db['users']
def main(username):
    with st.form("l15"):
        st.title("BOOK PUBLICATIONS")

        n1 = st.text_input("No. Of Books Published  upto previous assesment year:")
        st.write("Books Published in present assessment year:")
        aut = st.text_input("No of authors", value="", placeholder="Enter Number of Authors")
        pos = st.text_input("Position of authorship", value="", placeholder="Enter Position of authorship")
        iss = st.text_input("ISSN/ISBN No.", value="", placeholder="Enter ISSN/ISBN No.")
        lph = st.text_input("Level of Publishing House", value="", placeholder="Enter Level of Publishing House")
        tpb = st.text_input("Title and other particulars of the book", value="", placeholder="Enter Title and other particulars of the book")

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (n1 and aut and pos and iss and lph and tpb):
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
                    "books_published_previous": n1,
                    "authors": aut,
                    "position_of_authorship": pos,
                    "issn_isbn": iss,
                    "publishing_house_level": lph,
                    "book_particulars": tpb,
                    "department":department,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
