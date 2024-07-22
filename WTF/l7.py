import streamlit as st
import datetime
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l7']  # Replace 'l7' with your actual collection name
collection_users = db['users']  # Replace 'users' with your actual collection name for users

# Function to get points based on FDP type, funding type, and capacity
def get_points(fdp_type, funding_type, capacity):
    points_dict = {
        # International (>=2W)
        ("International (>=2W)", "External", "Convenor"): 100,
        ("International (>=2W)", "External", "Co-convenor"): 50,
        ("International (>=2W)", "External", "Sponsor"): 90,
        ("International (>=2W)", "External", "Internal"): 80,
        ("International (>=2W)", "Sponsor", "Convenor"): 90,
        ("International (>=2W)", "Sponsor", "Co-convenor"): 45,
        ("International (>=2W)", "Sponsor", "Sponsor"): 80,
        ("International (>=2W)", "Sponsor", "Internal"): 70,
        ("International (>=2W)", "Internal", "Convenor"): 80,
        ("International (>=2W)", "Internal", "Co-convenor"): 40,
        ("International (>=2W)", "Internal", "Sponsor"): 70,
        ("International (>=2W)", "Internal", "Internal"): 60,
        
        # National (>=2W)
        ("National (>=2W)", "External", "Convenor"): 90,
        ("National (>=2W)", "External", "Co-convenor"): 45,
        ("National (>=2W)", "External", "Sponsor"): 80,
        ("National (>=2W)", "External", "Internal"): 70,
        ("National (>=2W)", "Sponsor", "Convenor"): 80,
        ("National (>=2W)", "Sponsor", "Co-convenor"): 40,
        ("National (>=2W)", "Sponsor", "Sponsor"): 70,
        ("National (>=2W)", "Sponsor", "Internal"): 60,
        ("National (>=2W)", "Internal", "Convenor"): 70,
        ("National (>=2W)", "Internal", "Co-convenor"): 35,
        ("National (>=2W)", "Internal", "Sponsor"): 60,
        ("National (>=2W)", "Internal", "Internal"): 50,
        
        # International (1W to 2W)
        ("International (1W to 2W)", "External", "Convenor"): 90,
        ("International (1W to 2W)", "External", "Co-convenor"): 45,
        ("International (1W to 2W)", "External", "Sponsor"): 80,
        ("International (1W to 2W)", "External", "Internal"): 70,
        ("International (1W to 2W)", "Sponsor", "Convenor"): 80,
        ("International (1W to 2W)", "Sponsor", "Co-convenor"): 40,
        ("International (1W to 2W)", "Sponsor", "Sponsor"): 70,
        ("International (1W to 2W)", "Sponsor", "Internal"): 60,
        ("International (1W to 2W)", "Internal", "Convenor"): 70,
        ("International (1W to 2W)", "Internal", "Co-convenor"): 35,
        ("International (1W to 2W)", "Internal", "Sponsor"): 60,
        ("International (1W to 2W)", "Internal", "Internal"): 50,
        
        # National (1W to 2W)
        ("National (1W to 2W)", "External", "Convenor"): 80,
        ("National (1W to 2W)", "External", "Co-convenor"): 40,
        ("National (1W to 2W)", "External", "Sponsor"): 70,
        ("National (1W to 2W)", "External", "Internal"): 60,
        ("National (1W to 2W)", "Sponsor", "Convenor"): 70,
        ("National (1W to 2W)", "Sponsor", "Co-convenor"): 35,
        ("National (1W to 2W)", "Sponsor", "Sponsor"): 60,
        ("National (1W to 2W)", "Sponsor", "Internal"): 50,
        ("National (1W to 2W)", "Internal", "Convenor"): 60,
        ("National (1W to 2W)", "Internal", "Co-convenor"): 30,
        ("National (1W to 2W)", "Internal", "Sponsor"): 50,
        ("National (1W to 2W)", "Internal", "Internal"): 40,
        
        # International (<1W)
        ("International (<1W)", "External", "Convenor"): 80,
        ("International (<1W)", "External", "Co-convenor"): 40,
        ("International (<1W)", "External", "Sponsor"): 70,
        ("International (<1W)", "External", "Internal"): 60,
        ("International (<1W)", "Sponsor", "Convenor"): 70,
        ("International (<1W)", "Sponsor", "Co-convenor"): 35,
        ("International (<1W)", "Sponsor", "Sponsor"): 60,
        ("International (<1W)", "Sponsor", "Internal"): 50,
        ("International (<1W)", "Internal", "Convenor"): 60,
        ("International (<1W)", "Internal", "Co-convenor"): 30,
        ("International (<1W)", "Internal", "Sponsor"): 50,
        ("International (<1W)", "Internal", "Internal"): 40,
        
        # National (<1W)
        ("National (<1W)", "External", "Convenor"): 70,
        ("National (<1W)", "External", "Co-convenor"): 35,
        ("National (<1W)", "External", "Sponsor"): 60,
        ("National (<1W)", "External", "Internal"): 50,
        ("National (<1W)", "Sponsor", "Convenor"): 60,
        ("National (<1W)", "Sponsor", "Co-convenor"): 30,
        ("National (<1W)", "Sponsor", "Sponsor"): 50,
        ("National (<1W)", "Sponsor", "Internal"): 40,
        ("National (<1W)", "Internal", "Convenor"): 50,
        ("National (<1W)", "Internal", "Co-convenor"): 25,
        ("National (<1W)", "Internal", "Sponsor"): 40,
        ("National (<1W)", "Internal", "Internal"): 30,
    }
    
    return points_dict.get((fdp_type, funding_type, capacity), 0)

def main(username):
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    today = datetime.datetime.now()

    with st.form("l7"):
        st.title("FDPs Organized")
        
        fdp_types = ["International (>=2W)", "National (>=2W)", "International (1W to 2W)", 
                     "National (1W to 2W)", "International (<1W)", "National (<1W)"]
        funding_types = ["External", "Sponsor", "Internal"]
        capacities = ["Convenor", "Co-convenor", "Sponsor", "Internal"]
        
        fdp_type = st.selectbox(
            "Type of FDP",
            options=fdp_types,
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

        funding_type = st.selectbox(
            "Type of Funding",
            options=funding_types,
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

        capacity = st.selectbox(
            "Organised in the Capacity of",
            options=capacities,
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )

        frod = st.date_input("FDP STARTED DATE", today, format="MM.DD.YYYY")
        tod = st.date_input("FDP END DATE", today, format="MM.DD.YYYY")
        
        days = st.text_input("No of Days", value="", placeholder="Enter Number of Days")
        
        web_link = st.text_input("Enter Your FDP Web Link", value="", placeholder="Enter Web Link (e.g. https://example.com)")

        # Calculate points based on the selected options
        points = get_points(fdp_type, funding_type, capacity)



        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not fdp_type or not funding_type or not capacity or not days or not web_link:
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
                    "fdp_type": fdp_type,
                    "funding_type": funding_type,
                    "capacity_organised": capacity,
                    "start_date": frod.strftime("%Y-%m-%d"),
                    "end_date": tod.strftime("%Y-%m-%d"),
                    "no_of_days": days,
                    "fdp_web_link": web_link,
                    "points": points,  # Add points to the data
                    "department": department,
                    "date": datetime.datetime.now()
                }
                
                collection.insert_one(data)
                st.success("Data inserted successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
  # Replace 'your_username' with the actual username
    main(st.session_state.username)
