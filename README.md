# Animal Classification - CNN-based Cat & Dog Recognition 🐱🐶

This project is a deep learning-based image classification system that identifies whether an image containes a cat or a dog. It is build on a custom Convolutional Neural Network trained on an image dataset and is fully deployed using FastAPI for the backend and Streamlit for the frontend, both containerized with Docker. 

## Features
* Custom CNN Model: Designed and trained from scratch for high accuracy.
* FastAPI Backend: Handles image processing and model inference.
* Streamlit Frontend: Provides a user-friendly interface for uploading images and viewing predictions.
* Dockerized Deployment: Both frontend and backend run in separate Docker containers.
* Azure Integration: Images are stored in the Azure Storage Blob.

## How It Works
1. User uploads an image via the Streamlit web app.
2. The image is sent to the FastAPI backend.
3. The CNN model processes the image and returns a prediction (cat or dog).
4. The result is displayed in the frontend.
5. The data of the image is stored in the database
6. The image is uploaded to Azure Storage Blob.

## Deployment
* The backend listens on port 8000.
* The frontend runs on port 8501 and communicates with the backend.

## How to use 
### 1. Clone the Repository
```bash
git clone https://github.com/Jakubkmn/Animal-Classification.git
cd Animal-Classification
```
### 2. Setup the .env for the Azure integration

### 3. Build and Start the Containers
```bash
docker-compose up --build
```

### 4. Access the Application
* Frontend (Streamlit UI): http://localhost:8501
* Backend API (FastAPI Docs): http://localhost:8000/docs

### 5. Upload an Image
1. Opent the web app (localhost:8501)
2. Upload an image of a cat or a dog
3. View the prediction result
![image](https://github.com/user-attachments/assets/ed10ca6c-28a0-44fc-93ee-d66894bb6c32)


