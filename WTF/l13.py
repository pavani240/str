import streamlit as st
from pymongo import MongoClient
import datetime
import base64

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name
collection = db['l13']  # Replace 'lll02' with your actual collection name
collection_users = db['users']

def calculate_conference_points(proceeding_type, venue_location, authorship_position):
    points_dict = {
        "IEEE/Springer or equivalent": {
            "India": {
                "> University Level": {"1st author": 80, "other": 10},
                "University Level": {"1st author": 70, "other": 10},
                "College Level": {"1st author": 60, "other": 5}
            },
            "Abroad": {
                "> University Level": {"1st author": 100, "other": 20},
                "University Level": {"1st author": 90, "other": 20},
                "College Level": {"1st author": 80, "other": 10}
            }
        },
        "Other Conferences": {
            "India": {
                "> University Level": {"1st author": 40, "other": 5},
                "University Level": {"1st author": 30, "other": 5},
                "College Level": {"1st author": 20, "other": 5}
            },
            "Abroad": {
                "> University Level": {"1st author": 50, "other": 10},
                "University Level": {"1st author": 40, "other": 10},
                "College Level": {"1st author": 30, "other": 5}
            }
        }
    }
    return points_dict.get(proceeding_type, {}).get(venue_location, {}).get(authorship_position, 0)

def main(username):
    with st.form("l13"):
        st.title("No. Of CONFERENCE PUBLICATIONS in present assessment year:")

        st.write("Conference Publication Details")
        ath = st.text_input("No of authors", value="", placeholder="Enter Number of Authors")
        pat = st.text_input("Position of authorship", value="", placeholder="Enter Position of Authorship")
        pven = st.text_input("Venue of Conference", value="", placeholder="Enter Conference Venue")
        Jtype = st.selectbox("Venue at India/Abroad", ["", "India", "Abroad"])
        ptype = st.selectbox("Proceedings type", ["", "IEEE/Springer or equivalent", "Other Conferences"])
        venue_level = st.selectbox("Venue Level", ["", "> University Level", "University Level", "College Level"])
        
        # File uploader for PDF
        pdf_uploader = st.file_uploader("Upload your work in PDF", type=["pdf"])

        if st.form_submit_button("Submit"):
            # Check for empty fields
            if not (ath and pat and pven and Jtype and ptype and venue_level):
                st.error("Please fill out all required fields.")
                return

            if not pdf_uploader:
                st.error("Please upload the PDF.")
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

                # Read the file content and encode it in base64
                pdf_content = pdf_uploader.read()
                encoded_pdf = base64.b64encode(pdf_content).decode('utf-8')

                # Calculate points
                points = calculate_conference_points(ptype, Jtype, "1st author" if pat.lower() == "1st" else "other")

                data = {
                    "username": username,
                    "number_of_authors": ath,
                    "position_of_authorship": pat,
                    "conference_venue": pven,
                    "venue_location": Jtype,
                    "proceedings_type": ptype,
                    "venue_level": venue_level,
                    "pdf": encoded_pdf,
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
