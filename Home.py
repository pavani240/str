import connection
import streamlit as st
st.markdown("""
    <style>
        .st-emotion-cache-1huvf7z ef3psqc5{
            display: none !important;
        }
        .st-emotion-cache-1huvf7z ef3psqc5{
            display: none !important;
        }
        .justified-text {
            text-align: justify;
            margin-left: auto;
            margin-right: auto;
            max-width: 700px; /* Adjust the width as needed */
        }
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh; /* Adjust the height as needed */
        }
        }
    </style>
""", unsafe_allow_html=True)
st.subheader("Welcome to EvalMaster - Employee Appraisal Systems")
st.image('logo2.png')
st.markdown("""
        <div class="justified-text">
            To streamline and modernize the faculty appraisal process, our college has developed an
            innovative Faculty Appraisal System utilizing cutting-edge web technologies. This system
            addresses the inefficiencies and costs associated with the traditional paper-based appraisal
            method, aiming to significantly reduce paper consumption and administrative overhead. The
            Faculty Appraisal System features a user-friendly interface, where detailed faculty profiles
            serve as comprehensive repositories of achievements, qualifications, and performance metrics,
            allowing faculty members to update their profiles annually. The Faculty Appraisal System
            leverages secure and scalable web technologies, ensuring data integrity and security while
            safeguarding sensitive information from unauthorized access. This transition to a digital system
            aligns with our commitment to sustainability by reducing reliance on paper, contributing to
            environmental conservation, and promoting eco-friendly practices. Additionally, it offers
            significant time savings for faculty members and administrative staff, enhancing efficiency and
            transparency in faculty evaluations. This innovative system not only reduces costs and
            administrative burdens but also ensures fair and comprehensive appraisals, serving as a model
            for other institutions seeking to modernize their appraisal processes.
        </div>
    """, unsafe_allow_html=True)
st.markdown("""
    <style>
        .footer {
            
            position: relative;
            bottom: 0;
            width: 100%;    
            text-align: right;
            padding: 10px;
            font-size: 12px;
        }
    </style>
    <div class="footer">
        © 2024 Aditya Institute of Technology & Management.All rights reserved.
    </div>
""", unsafe_allow_html=True)