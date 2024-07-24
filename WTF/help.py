import streamlit as st

def main():
    st.title("Help Page")
    
    st.header("Introduction")
    st.write(
        """
        Welcome to the Streamlit application! This application allows you to manage various aspects of your data with ease.
        Below, you'll find information on how to use the features and navigate the app.
        """
    )
    
    st.header("Features")
    st.write(
        """
        - **l 1**: THEORY COURSES HANDLED.
        - **l 2**: STUDENT PROJECT WORKS UNDERTAKEN.
        - **l 3**: STUDENT TRAINING.
        """
    )
    
    st.header("How to Use")
    st.write(
        """
        1. **Login**: Start by logging in with your credentials.
        2. **Navigation**: Use the sidebar to navigate between different sections.
        3. **Data Entry**: Fill out forms and submit data as required.
        4. **Viewing Data**: Access and view your data through various views.
        """
    )
    
    st.header("FAQs")
    st.write(
        """
        - **How do I reset my password?**
          - Contact Admin.

        - **Where can I find more detailed documentation?**
          - Detailed documentation is available under the "Documentation" section.

        - **Who can I contact for support?**
          - Reach out to our support team at support@example.com.
          - Fill the issue form that will be available at the end of your pages to contact admin.
        """
    )
    
    st.header("Contact Information")
    st.write(
        """
        For any additional questions or support, please contact us at:
        - **Email**: support@example.com
        - **Phone**: +123 456 7890
        """
    )

if __name__ == "__main__":
    main()
