import streamlit as st
import requests
from PIL import Image
import io

st.title("Dog or Cat Classifier")

uploaded_file = st.file_uploader("Upload an image of a dog or cat", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")
    
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')  # Save as JPEG to match backend requirements
    img_byte_arr.seek(0)  # Reset pointer to the beginning of the stream

    files = {'file': ('uploaded_image.jpg', img_byte_arr, 'image/jpeg')}
    response = requests.post("http://127.0.0.1:8000/predict/", files=files)

    if response.status_code == 200:
        prediction = response.json()
        st.write(f"Prediction: {prediction['prediction']}")
    else:
        st.write("Error in prediction: " + response.text)