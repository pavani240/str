# import mysql.connector
# connection=mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='',
#     database='strea'
# )
# if(connection):
#     print("connected")
# Remove or comment out MySQL connection code
# import mysql.connector

# connection = mysql.connector.connect(
#     host="localhost",
#     user="youruser",
#     password="yourpassword",
#     database="yourdatabase"
# )

# Add MongoDB connection if needed
from pymongo import MongoClient

client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")

db = client['Streamlit']
