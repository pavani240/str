import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']  # Replace 'Streamlit' with your actual database name

# List of collections
collections = [
    'l1', 'l2', 'l3', 'l4', 'l5', 'll1', 'll2', 'll3', 'll4', 
    'll5', 'll6', 'lll01', 'lll02', 'lll03', 'lll04', 'lll05', 'lll06', 'lll07'
]

def date_to_datetime(date):
    return datetime.combine(date, datetime.min.time())

def retrieve_data_from_collection(username, collection_name, start_date=None, end_date=None):
    collection = db[collection_name]
    query = {"username": username}
    
    # Apply date filter to query    
    if start_date and end_date:
        start_datetime = date_to_datetime(start_date)
        end_datetime = date_to_datetime(end_date)
        query["timestamp"] = {"$gte": start_datetime, "$lte": end_datetime}
    
    projection = {"_id": 0}  # Exclude the id field
    data = list(collection.find(query, projection))
    return data

def insert_notification(username, comment):
    notification_collection = db['notifications']
    notification = {
        "username": username,
        "message": comment,
        "category": "faculty",
        "timestamp": datetime.now()
    }
    try:
        result = notification_collection.insert_one(notification)
        st.success("Notification successfully submitted.")
    except Exception as e:
        st.error(f"Error inserting notification: {e}")

def main():
    st.title("Retrieval and Notification Page")
    
    # Enter username to search
    username = st.text_input("Enter username to search:")
    
    if not username:
        st.warning("Please enter a username.")
        return
    
    # Date filter inputs
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    
    # Select collection(s) to retrieve data from
    selected_collections = st.multiselect("Select Collection(s)", collections, default=collections)

    # Flags to track if data retrieval buttons were clicked
    retrieve_clicked = False
    retrieve_all_clicked = False
    
    # Use st.columns() to place buttons side by side
    col1, col2 = st.columns(2)
    
    # "Retrieve" button
    if col1.button("Retrieve"):
        retrieve_clicked = True
        try:
            for collection_name in selected_collections:
                st.subheader(f"Collection: {collection_name.upper()}")
                data = retrieve_data_from_collection(username, collection_name, start_date, end_date)
                
                if not data:
                    st.warning(f"No data found for username '{username}' in collection '{collection_name}'.")
                else:
                    df = pd.DataFrame(data)
                    st.dataframe(df)
                    st.write("")  # Empty line for spacing
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # "Retrieve All Data" button
    if col2.button("Retrieve All Data"):
        retrieve_all_clicked = True
        try:
            for collection_name in selected_collections:
                st.subheader(f"Collection: {collection_name.upper()}")
                data = retrieve_data_from_collection(username, collection_name)
                
                if not data:
                    st.warning(f"No data found for username '{username}' in collection '{collection_name}'.")
                else:
                    df = pd.DataFrame(data)
                    st.dataframe(df)
                    st.write("")  # Empty line for spacing
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
    st.warning("Please fill after careful review.")
    # Display comment entry and submit button using st.form
    with st.form(key='comment_form'):
        st.write("")  # Empty line for spacing
        comment = st.text_area("Enter your comment:", height=100)
        submit_button = st.form_submit_button("Submit Comment")
        
        if submit_button and comment:
            insert_notification(username, comment)
        elif submit_button:
            st.warning("Please enter a comment.")
    
if __name__ == "__main__":
    main()
