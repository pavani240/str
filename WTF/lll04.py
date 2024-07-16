import streamlit as st
from pymongo import MongoClient
import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['lll04']  # Replace 'lll04' with your actual collection name

def main():
    with st.form("lll4"):
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
                data = {
                    "books_published_previous": n1,
                    "authors": aut,
                    "position_of_authorship": pos,
                    "issn_isbn": iss,
                    "publishing_house_level": lph,
                    "book_particulars": tpb,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
