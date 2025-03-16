import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(page_title="Home page", page_icon="🐱🐶")

st.sidebar.header("Home page")

st.title("Dog or Cat Classifier")

uploaded_file = st.file_uploader("Upload an image of a dog or cat", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if uploaded_file is not None:
    for file in range(len(uploaded_file)):
        image = Image.open(uploaded_file[file])
        st.image(image, caption=uploaded_file[file].name)
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')  # Save as JPEG to match backend requirements
        img_byte_arr.seek(0)  # Reset pointer to the beginning of the stream

        files = {'file': ('uploaded_image.jpg', img_byte_arr, 'image/jpeg')}
        response = requests.post("http://backend_service:8000/predict/", files=files)

        if response.status_code == 200:
            prediction = response.json()
            st.subheader(f"The model is {prediction['confidence']:.1f}% confident that the image shows a {prediction['prediction'].capitalize()}")
        else:
            st.write("Error in prediction: " + response.text)
