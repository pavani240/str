import streamlit as st
import datetime
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['ll1']  # Replace 'll1' with your actual collection name

def main():
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
    
    today = datetime.datetime.now()

    with st.form("ll1"):   
        st.title("FDPs Attended")
        
        Subject = st.text_input("Name of the FDP", value="", placeholder="Enter FDP Name")
        sins = st.text_input("Level Of Institute", value="", placeholder="Enter Level")
        title = st.text_input("Title of Event", value="", placeholder="Enter event title")
        ht = st.text_input("Host Institution", value="", placeholder="Enter host institution")
        
        frod = st.date_input("FDP STARTED DATE", datetime.datetime.now(), format="MM.DD.YYYY")
        tod = st.date_input("FDP END DATE", datetime.datetime.now(), format="MM.DD.YYYY")
        
        days = st.text_input("No of Days", value="", placeholder="Enter event no of days")
        
        option1 = st.selectbox(
            "Duration of the FDP",
            (">=2W", "1W-2W", "<1W"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
        
        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not Subject or not sins or not title or not ht or not days:
                st.error("Please fill out all required fields.")
                return

            try:
                data = {
                    "fdp_name": Subject,
                    "institute_level": sins,
                    "event_title": title,
                    "host_institution": ht,
                    "start_date": frod.strftime("%Y-%m-%d"),
                    "end_date": tod.strftime("%Y-%m-%d"),
                    "no_of_days": days,
                    "fdp_duration": option1,
                    "date":datetime.datetime.now()
                }
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
