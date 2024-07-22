import streamlit as st
from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l15']  # Replace 'lll04' with your actual collection name
collection_users = db['users']

def calculate_book_points(issn_isbn, position_of_authorship, publishing_house_level):
    is_international = "International" in publishing_house_level
    has_isbn = issn_isbn.strip().upper() == "YES"
    is_first_author = "1st" in position_of_authorship.lower()

    if is_international:
        if has_isbn:
            return 100 if is_first_author else 25
        else:
            return 50 if is_first_author else 10
    else:
        if has_isbn:
            return 75 if is_first_author else 10
        else:
            return 35 if is_first_author else 5

def main(username):
    with st.form("l15"):
        st.title("BOOK PUBLICATIONS")

        n1 = st.text_input("No. Of Books Published up to the previous assessment year:")
        st.write("Books Published in present assessment year:")
        aut = st.text_input("No of authors", value="", placeholder="Enter Number of Authors")
        pos = st.text_input("Position of authorship", value="", placeholder="Enter Position of authorship (e.g., 1st author, co-author)")
        iss = st.selectbox("ISSN/ISBN No.", ["", "YES", "NO"])
        lph = st.text_input("Level of Publishing House", value="", placeholder="Enter Level of Publishing House (e.g., International Publisher, National Publisher)")
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
                
                # Calculate points
                points = calculate_book_points(iss, pos, lph)

                data = {
                    "username": username,
                    "books_published_previous": n1,
                    "authors": aut,
                    "position_of_authorship": pos,
                    "issn_isbn": iss,
                    "publishing_house_level": lph,
                    "book_particulars": tpb,
                    "department": department,
                    "points": points,
                    "date": datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success(f"Data inserted successfully! Total Points: {points}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main(st.session_state.username)
