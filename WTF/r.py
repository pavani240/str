import streamlit as st
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

def main():
    st.title("Retrieve Forwarded Data")

    # Retrieve data from the 'forwarded' collection and sort by timestamp descending
    forwarded_data = list(db['forwarded'].find({}, {'_id': 0}).sort("timestamp", -1))

    if forwarded_data:
        # Convert the data to a DataFrame
        df = pd.DataFrame(forwarded_data)
        
        for index, row in df.iterrows():
            st.write("### Forwarded Data Entry")
            for col in df.columns:
                # Ensure each text input has a unique key
                st.text_input(f"{col}_{index}", row[col], disabled=True)
            
            # Buttons for approve and write review
            if st.button(f"Approve_{index}"):
                update_status(row['username'], "approved")
                st.success(f"Status updated to 'approved' for {row['username']}.")

            if st.button(f"Write Review_{index}"):
                st.session_state[f"show_review_form_{index}"] = True

            # Display the review form if the button was clicked
            if st.session_state.get(f"show_review_form_{index}", False):
                with st.form(key=f"review_form_{index}", clear_on_submit=True):
                    review = st.text_area("Enter your review:")
                    submit = st.form_submit_button("Submit Review")

                    if submit:
                        update_status(row['username'], "reviewed", review)
                        st.success(f"Review submitted for {row['username']}.")
                        st.session_state[f"show_review_form_{index}"] = False

    else:
        st.write("No data found in the 'forwarded' collection.")

def update_status(username, status, review=None):
    status_collection = db['status']
    status_data = {
        "username": username,
        "status": status,
        "timestamp": datetime.now()
    }
    if review:
        status_data["review"] = review

    try:
        result = status_collection.insert_one(status_data)
        print(f"Status updated with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error updating status: {e}")

if __name__ == "__main__":
    main()
