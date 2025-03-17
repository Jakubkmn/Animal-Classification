import streamlit as st
import requests

st.set_page_config(page_title="gallery")

st.sidebar.header("Gallery")

response = requests.get("http://backend_service:8000/gallery")

if response.status_code == 200:
    images = response.json()['images']
    for image in images:
        st.image(image["data"])
else:
    st.write(f"Error {response.text}")