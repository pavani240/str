import streamlit as st
from pymongo import MongoClient
import pandas as pd
import importlib
from WTF import l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, retrieve, facultyretrieve, notification, HODD, sent, r, pdf

st.markdown("""
    <style>
        .st-emotion-cache-1wbqy5l e3g6aar2{
            display: none !important;
        }
        .st-emotion-cache-1huvf7z ef3psqc5{
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

client = MongoClient("mongodb+srv://devicharanvoona1831:HSABL0BOyFNKdYxt@cluster0.fq89uja.mongodb.net/")
db = client['Streamlit']

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["HOD", "Faculty", "Principal", "Admin"])

    if st.button("Login"):
        user = db['users'].find_one({"username": username, "password": password, "role": role})
        if user:
            if user.get('role') == "Suspended":
                st.error("You are no longer part of the organization.")
            else:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.password = password
                st.session_state.role = role
                st.experimental_rerun()
        else:
            st.error("Invalid username, password, or role")

def hod_home():
    st.title(f"Welcome HOD: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    nav = st.sidebar.radio("Navigation", ["Faculty Details", "Received", "Sent", "Retrieved Data", "Pdf View", "Departmental Retrieve"])

    if nav == "Faculty Details":
        show_faculty_details()
    elif nav == "Received":
        st.write("Received Page")
    elif nav == "Sent":
        sent.main()
    elif nav == "Pdf View":
        pdf.main()
    elif nav == "Retrieved Data":
        retrieve.main()
    elif nav == "Departmental Retrieve":
        HODD.main(st.session_state.username)

def principal_home():
    st.title(f"Welcome Principal: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    nav = st.sidebar.radio("Navigation", ["Faculty Details", "Received", "Pdf View", "Sent"])

    if nav == "Faculty Details":
        show_faculty_details()
    elif nav == "Received":
        r.main()
    elif nav == "Pdf View":
        pdf.main()
    elif nav == "Sent":
        st.write("No sent page")

def faculty_home():
    st.title(f"Welcome Faculty: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    available_pages = ["l1", "l2", "l3", "l4", "l5", "l6", "l7", "l8", "l9", "l10", "l11", "l12", "l13", "l14", "l15", "l16", "l17", "l18", "Retrieve", "Notifications"]
    nav = st.sidebar.radio("Navigation", available_pages)

    if nav == "l1":
        l1.main(st.session_state.username)
    elif nav == "l2":
        l2.main()
    elif nav == "l3":
        l3.main()
    elif nav == "l4":
        l4.main(st.session_state.username)
    elif nav == "l5":
        l5.main(st.session_state.username)
    elif nav == "l6":
        l6.main(st.session_state.username)
    elif nav == "l7":
        l7.main(st.session_state.username)
    elif nav == "l8":
        l8.main(st.session_state.username)
    elif nav == "l9":
        l9.main(st.session_state.username)
    elif nav == "l10":
        l10.main(st.session_state.username)
    elif nav == "l11":
        l11.main(st.session_state.username)
    elif nav == "l12":
        l12.main(st.session_state.username)
    elif nav == "l13":
        l13.main(st.session_state.username)
    elif nav == "l14":
        l14.main(st.session_state.username)
    elif nav == "l15":
        l15.main(st.session_state.username)
    elif nav == "l16":
        l16.main(st.session_state.username)
    elif nav == "l17":
        l17.main(st.session_state.username)
    elif nav == "l18":
        l18.main(st.session_state.username)
    elif nav == "Retrieve":
        facultyretrieve.main(st.session_state.username)
    elif nav == "Notifications":
        notification.main(st.session_state.username)

def admin_home():
    st.title(f"Welcome Admin: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    nav = st.sidebar.radio("Navigation", ["Add User", "Suspend User"])

    if nav == "Add User":
        add_user_form()
    elif nav == "Suspend User":
        suspend_user_form()

def add_user_form():
    st.header("Add New User")

    with st.form("add_user_form"):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        new_role = st.selectbox("Role", ["Faculty", "HOD", "Principal"])
        new_department = st.text_input("Department")

        submit_button = st.form_submit_button("Add User")

        if submit_button:
            if new_username and new_password and new_role and new_department:
                new_user = {
                    "username": new_username,
                    "password": new_password,
                    "role": new_role,
                    "department": new_department,
                    "status": "Active"  # Default status
                }
                try:
                    db['users'].insert_one(new_user)
                    st.success("User added successfully!")
                except Exception as e:
                    st.error(f"Error adding user: {e}")
            else:
                st.warning("Please fill in all fields.")

def suspend_user_form():
    st.header("Suspend User")

    with st.form("suspend_user_form"):
        suspend_username = st.text_input("Username to Suspend")

        submit_button = st.form_submit_button("Suspend User")

        if submit_button:
            if suspend_username:
                try:
                    result = db['users'].update_one(
                        {"username": suspend_username},
                        {"$set": {"role": "Suspended"}}
                    )
                    if result.matched_count > 0:
                        st.success(f"User '{suspend_username}' has been suspended successfully!")
                    else:
                        st.warning(f"User '{suspend_username}' not found.")
                except Exception as e:
                    st.error(f"Error suspending user: {e}")
            else:
                st.warning("Please enter a username.")

def show_faculty_details():
    # Retrieve the department of the logged-in HOD
    if st.session_state.role == "HOD":
        hod_department = db['users'].find_one({"username": st.session_state.username})['department']
        # Filter users based on the HOD's department
        users = db['users'].find({"department": hod_department})
        
        # Define the columns to display
        columns_to_display = ["username", "role", "department"]
    else:
        # For other roles, display all users
        users = db['users'].find()
        columns_to_display = ["username", "password", "role", "department"]
    
    # Convert the result to a DataFrame
    df = pd.DataFrame(list(users), columns=["username", "password", "role", "department"])
    
    # Display the DataFrame with selected columns
    st.write(df[columns_to_display])

def show_page(page_name):
    try:
        module = importlib.import_module(page_name)
        module.main()
    except ModuleNotFoundError:
        st.error(f"Page '{page_name}' not found.")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.experimental_rerun()

if not st.session_state.logged_in:
    login()
else:
    if st.session_state.role == "HOD":
        hod_home()
    elif st.session_state.role == "Principal":
        principal_home()
    elif st.session_state.role == "Faculty":
        faculty_home()
    elif st.session_state.role == "Admin":
        admin_home()
