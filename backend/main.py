from fastapi import FastAPI, UploadFile
from fastapi.responses import RedirectResponse
from PIL import Image
import tensorflow as tf
import numpy as np
import io
import os

app = FastAPI()

model_path = os.path.join(os.path.dirname(__file__), "my_model.keras")
model = tf.keras.models.load_model(model_path)

@app.post("/uploadfiles/", include_in_schema=False)
async def upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/docs")

@app.post("/predict")
async def predict(file: UploadFile):
    contents = await file.read() # Returns bytes
    img = Image.open(io.BytesIO(contents)).convert('RGB')
    img = img.resize((128,128))
    image_array = np.array(img)
    image_array = np.expand_dims(image_array, axis=0)

    prediction = model.predict(image_array)

    label = "dog" if prediction[0][0] > 0.5 else "cat"
    return {"prediction": label, "confidence": float(prediction[0][0])}