# Initialize session state variables
import streamlit as st
from pymongo import MongoClient
import pandas as pd
import importlib
from WTF import l1, l2, l3, l4, l5, ll1, ll2, ll3, ll4, ll5, ll6, lll01, lll02, lll03, lll04, lll05, lll06, lll07, retrieve, facultyretrieve, notification, HODD, sent, r
st.markdown("""
    <style>
        .st-emotion-cache-1wbqy5l e3g6aar2{
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

    nav = st.sidebar.radio("Navigation", ["Faculty Details", "Received", "Sent", "Retrieved Data", "Retrieve All Data","Departmental Retrieve"])

    if nav == "Faculty Details":
        show_faculty_details()
    elif nav == "Received":
        st.write("Received Page")
    elif nav == "Sent":
        sent.main()
    # elif nav == "Pending":
    #     st.write("Pending Page")
    elif nav == "Retrieved Data":
        retrieve.main()
    elif nav == "Departmental Retrieve":
        HODD.main(st.session_state.username)

def principal_home():
    st.title(f"Welcome Principal: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    nav = st.sidebar.radio("Navigation", ["Faculty Details", "Received", "Sent"])

    if nav == "Faculty Details":
        show_faculty_details()
    elif nav == "Received":
        r.main()
    elif nav == "Sent":
        st.write("No sent page")
    # elif nav == "Pending":
    #     st.write("Pending Page")

def faculty_home():
    st.title(f"Welcome Faculty: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        logout()

    available_pages = ["l1", "l2", "l3", "l4", "l5", "ll1", "ll2", "ll3", "ll4", "ll5", "ll6", "lll1", "lll2", "lll3", "lll4", "lll5", "lll6", "lll7", "Retrieve", "Notifications"]
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
        l5.main()
    elif nav == "ll1":
        ll1.main()
    elif nav == "ll2":
        ll2.main()
    elif nav == "ll3":
        ll3.main()
    elif nav == "ll4":
        ll4.main()
    elif nav == "ll5":
        ll5.main()
    elif nav == "ll6":
        ll6.main()
    elif nav == "lll1":
        lll01.main()
    elif nav == "lll2":
        lll02.main()
    elif nav == "lll3":
        lll03.main()
    elif nav == "lll4":
        lll04.main()
    elif nav == "lll5":
        lll05.main()
    elif nav == "lll6":
        lll06.main()
    elif nav == "lll7":
        lll07.main()
    elif nav == "Retrieve":
        facultyretrieve.main(st.session_state.username)
    elif nav == "Notifications":
        notification.main(st.session_state.username)

def show_faculty_details():
    result = list(db['faculty'].find())
    df = pd.DataFrame(result, columns=["id", "name", "department", "email"])  # Adjust column names based on your collection
    st.write(df)

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
