import streamlit as st
import requests
from PIL import Image
import io


# def display_images(uploaded_files):
#     num_columns = len(uploaded_files)
#     columns = st.columns(num_columns)

#     for idx, uploaded_file in enumerate(uploaded_files):
#         with columns[idx]:
#             image = Image.open(uploaded_file)
#             st.image(image, caption=uploaded_file.name)

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
        response = requests.post("http://127.0.0.1:8000/predict/", files=files)

        if response.status_code == 200:
            prediction = response.json()
            st.write(f"Prediction: {prediction['prediction']}")
        else:
            st.write("Error in prediction: " + response.text)
