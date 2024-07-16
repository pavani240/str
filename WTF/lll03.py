import streamlit as st
from pymongo import MongoClient
import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['lll03']  # Replace 'lll03' with your actual collection name

def main():
    with st.form("lll3"):
        st.title("RESEARCH GUIDANCE (Ph.D/M.Phil)")

        n1 = st.text_input("No. Of STUDENTS Completed Ph.D/M.Phil:")
        st.write("No. Of STUDENTS doing Ph.D/M.Phil in present assessment year:")
        deg = st.text_input("Degree", value="", placeholder="Enter Degree")
        uni = st.text_input("University", value="", placeholder="Enter University")
        gui = st.text_input("Guide/Co-Guide", value="", placeholder="Enter Guide/Co-Guide")
        frod3 = st.date_input(
            "Date of Registration",
            (datetime.datetime.now().date()),
            format="MM.DD.YYYY",
        )
        stype = st.text_input("Student Particulars", value="", placeholder="Enter Particulars Of Student")

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (n1 and deg and uni and gui and stype):
                st.error("Please fill out all required fields.")
                return
            
            try:
                # Convert date to datetime.datetime
                frod3 = datetime.datetime.combine(frod3, datetime.datetime.min.time())

                data = {
                    "students_completed": n1,
                    "degree": deg,
                    "university": uni,
                    "guide": gui,
                    "date_of_registration": frod3,
                    "student_particulars": stype,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
