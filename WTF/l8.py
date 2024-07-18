import streamlit as st
import datetime
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l8']  # Replace 'll3' with your actual collection name
collection_users=['users']
def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    today = datetime.datetime.now()

    with st.form("l8"):   
        st.title("PROFESSIONAL ROLES")
        
        Subject = st.text_input("Nature of work", value="", placeholder="Enter the Nature of Work")
        Subject3 = st.text_input("Type of funding", value="", placeholder="External, Sponsorships & Internal")
        
        frod = st.date_input("SINCE DATE (1)", datetime.datetime.now(), format="MM.DD.YYYY")
        
        st.write("Department level (HODs, College level section Incharges)") 
        Suhod = st.text_input("Department (2)", value="", placeholder="Enter Department")
        Subhodt3 = st.text_input("Nature of work (2)", value="", placeholder="Enter Nature of Work")
        frodd = st.date_input("SINCE DATE (2)", datetime.datetime.now(), format="MM.DD.YYYY")

        st.write("Department level Incharges & College level Committee Coordinators")
        Suhod1 = st.text_input("Department (3)", value="", placeholder="Enter Department")
        frod3 = st.date_input("SINCE DATE (3)", datetime.datetime.now(), format="MM.DD.YYYY")

        st.write("CURRENTLY engaged Committee Memberships")
        Suhod11 = st.text_input("Department (4)", value="", placeholder="Enter Department")
        frodt = st.date_input("SINCE DATE (4)", datetime.datetime.now(), format="MM.DD.YYYY")

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not Subject or not Subject3 or not Suhod or not Subhodt3 or not Suhod1 or not Suhod11:
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
                    "nature_of_work": Subject,
                    "type_of_funding": Subject3,
                    "since_date_1": frod.strftime("%Y-%m-%d"),
                    "hod_department": Suhod,
                    "hod_nature_of_work": Subhodt3,
                    "hod_since_date": frodd.strftime("%Y-%m-%d"),
                    "incharge_department": Suhod1,
                    "incharge_since_date": frod3.strftime("%Y-%m-%d"),
                    "membership_department": Suhod11,
                    "membership_since_date": frodt.strftime("%Y-%m-%d"),
                    "department":department,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
