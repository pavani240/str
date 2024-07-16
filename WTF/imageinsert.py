import streamlit as st
import connection as c



def upload_image_to_db(image_file, name):

    cursor = c.connection.cursor()
    insert_query = """INSERT INTO images (name, image) VALUES (%s, %s)"""
    image_data = image_file.read()
    cursor.execute(insert_query, (name, image_data))
    c.connection.commit()
    cursor.close()
    c.connection.close()

st.title("Upload Image")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_name = uploaded_file.name
    if st.button('Upload'):
        upload_image_to_db(uploaded_file, file_name)
        st.success("Image uploaded successfully!")
