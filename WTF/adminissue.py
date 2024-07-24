import streamlit as st
from pymongo import MongoClient
import pandas as pd

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']
issues_collection = db['issues']

def fetch_issues():
    return list(issues_collection.find())

def main():
    st.title("All Submitted Issues")

    issues = fetch_issues()

    if issues:
        df = pd.DataFrame(issues)
        df = df[['username', 'datetime', 'issue']]  # Select only the necessary columns
        df['datetime'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))  # Format datetime
        st.dataframe(df)
    else:
        st.write("No issues have been submitted yet.")

if __name__ == "__main__":
    main()
