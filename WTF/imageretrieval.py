import streamlit as st
import connection as c
from PIL import Image
import io

def fetch_images_from_db():
    connection = None
    cursor = None
    images = []
    try:
        
        cursor = c.connection.cursor()
        fetch_query = """SELECT id, name FROM images"""
        cursor.execute(fetch_query)
        images = cursor.fetchall()
    except Exception as e:
        st.error(f"Error fetching images: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            c.connection.close()
    return images

def fetch_image_by_id(image_id):
    connection = None
    cursor = None
    image_data = None
    try:
        
        cursor = c.connection.cursor()
        fetch_query = """SELECT image FROM images WHERE id = %s"""
        cursor.execute(fetch_query, (image_id,))
        image_data = cursor.fetchone()[0]
    except Exception as e:
        st.error(f"Error fetching image: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            c.connection.close()
    return image_data

st.title("Retrieve Image")

images = fetch_images_from_db()
image_dict = {name: image_id for image_id, name in images}

selected_image = st.selectbox("Select an image to view", list(image_dict.keys()))

if selected_image:
    image_id = image_dict[selected_image]
    image_data = fetch_image_by_id(image_id)
    if image_data:
        image = Image.open(io.BytesIO(image_data))
        st.image(image, caption=selected_image)
