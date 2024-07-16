import streamlit as st
import datetime
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['ll2']  # Replace 'll2' with your actual collection name

def main():
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
    
    today = datetime.datetime.now()

    with st.form("ll2"):   
        st.title("FDPs Organized")
        
        Subject = st.text_input("Type of FDP", value="", placeholder="Enter Type of FDP")
        Subject3 = st.text_input("Type of funding", value="", placeholder="External, Sponsorships & Internal")
        Subject2 = st.text_input("Organised in the capacity of", value="", placeholder="Enter capacity organised name")
        
        frod = st.date_input("FDP STARTED DATE", datetime.datetime.now(), format="MM.DD.YYYY")
        tod = st.date_input("FDP END DATE", datetime.datetime.now(), format="MM.DD.YYYY")
        
        days = st.text_input("No of days", value="", placeholder="Enter no of days")
        
        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not Subject or not Subject3 or not Subject2 or not days:
                st.error("Please fill out all required fields.")
                return

            try:
                data = {
                    "fdp_type": Subject,
                    "funding_type": Subject3,
                    "capacity_organised": Subject2,
                    "start_date": frod.strftime("%Y-%m-%d"),
                    "end_date": tod.strftime("%Y-%m-%d"),
                    "no_of_days": days,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
