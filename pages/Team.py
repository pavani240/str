import streamlit as st

def main():
    st.title('Developer and Guide Showcase')

    # Create columns for developers and guides
    col1, col2 = st.columns(2)

    # Developer 1 details
    with col1:
        st.subheader('Developer 1')
        st.image('pages/d2.png', width=200)
        st.markdown('**Name:** VEMAKOTI KRISHNAMURTY')
        st.markdown('**Mail:** krishnaias28@gmail.com')
        st.markdown('**Connect on:** [LinkedIn](https://in.linkedin.com/in/vemakoti-krishnamurty-9a9199235)')

    # Developer 2 details
    with col2:
        st.subheader('Developer 2')
        st.image('pages/d1.png', width=200)
        st.markdown('**Name:** VOONA DEVI CHARAN')
        st.markdown('**Mail:** devicharanvoona1831@gmail.com')
        st.markdown('**Connect on:** [LinkedIn](https://in.linkedin.com/in/voona-devicharan-34125522b)')

    # Guides
    st.header('Guides')
    col3, col4 = st.columns(2)

    # Guide 1
    with col3:
        st.subheader('Guide 1')
        st.image('pages/g2.png', width=200)
        st.markdown('**Name:** Dr. K Eswarrao')
        st.markdown('**Mail:** eswarkoppala@gmail.com')
        st.markdown('**Connect on:** [LinkedIn](https://www.linkedin.com/in/johndoe/)')

    # Developer 2 details
    with col4:
        st.subheader('Guide 2')
        st.image('pages/g1.png', width=200)
        st.markdown('**Name:** Sri B Ramesh')
        st.markdown('**Mail:** ramesh.bandaru15@gmail.com')
        st.markdown('**Connect on:** [LinkedIn](https://in.linkedin.com/in/ramesh-bandaru-a0634767)')


if __name__ == "__main__":
    main()
