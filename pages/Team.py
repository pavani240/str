import streamlit as st

def main():
    st.title('Developer and Guide Showcase')

    # Create columns for developers and guides
    col1, col2 = st.columns(2)

    # Developer 1 details
    with col1:
        st.header('Developer 1')
        st.image('pages/d2.png', width=200)
        st.markdown('**Name:** VEMAKOTI KRISHNAMURTY')
        st.markdown('[GitHub](https://github.com/johndoe) | [LinkedIn](https://www.linkedin.com/in/johndoe/)')

    # Developer 2 details
    with col2:
        st.header('Developer 2')
        st.image('pages/d1.png', width=200)
        st.markdown('**Name:** VOONA DEVI CHARAN')
        st.markdown('[GitHub](https://github.com/janesmith) | [LinkedIn](https://www.linkedin.com/in/janesmith/)')

    # Guides
    st.header('Guides')
    col3, col4 = st.columns(2)

    # Guide 1
    with col3:
        st.header('Guide 1')
        st.image('pages/g2.png', width=200)
        st.markdown('**Name:** Dr. K Eswarrao')
        st.markdown('[GitHub](https://github.com/johndoe) | [LinkedIn](https://www.linkedin.com/in/johndoe/)')

    # Developer 2 details
    with col4:
        st.header('Guide 2')
        st.image('pages/g1.png', width=200)
        st.markdown('**Name:** Sri B Ramesh')
        st.markdown('[GitHub](https://github.com/janesmith) | [LinkedIn](https://www.linkedin.com/in/janesmith/)')


if __name__ == "__main__":
    main()
