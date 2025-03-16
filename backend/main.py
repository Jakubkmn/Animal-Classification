from fastapi import FastAPI, UploadFile, Depends
from fastapi.responses import RedirectResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime, timezone
from typing import Annotated, Optional
from PIL import Image
import tensorflow as tf
import numpy as np
import io
import os

sqlite_file_name = 'database.session'
sqlite_url = f'sqlite:///{sqlite_file_name}'
connect_args = {'check_same_thread':False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

class IMGDB(SQLModel, table=True):
    id : int = Field(default=None, primary_key=True)
    label : str = Field(default=None)
    confidence : float = Field(default=None)
    timestamps : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    image_url : str = Field(default=None)

app = FastAPI()

model_path = os.path.join(os.path.dirname(__file__), "my_model.keras")
model = tf.keras.models.load_model(model_path)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/uploadfiles/", include_in_schema=False)
async def upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}

@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse("/docs")

@app.post("/predict")
async def predict(file: UploadFile, session: SessionDep):
    contents = await file.read() # Returns bytes
    label, confidence = predict_image(image_bytes=contents)

    image_url = "pw.edu.pl"

    # image_url = upload_to_azure(file.filename, image_bytes)

    record = save_to_database(label, confidence=confidence, image_url=image_url, session=session)

    return {"prediction": label, "confidence": confidence, "image_url": image_url}

@app.get('/images')
async def show_images(session: SessionDep):
    images = session.exec(select(IMGDB)).all()
    return images

def predict_image(image_bytes: bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((128,128))
    image_array = np.array(img)
    image_array = np.expand_dims(image_array, axis=0)
    prediction = model.predict(image_array)
    label = 'dog' if prediction[0][0] > 0.5 else "cat"
    confidence = float(prediction[0][0]) * 100 if label == 'dog' else float(1 - prediction[0][0]) * 100
    return label, confidence

def save_to_database(label: str, confidence: float, image_url: str, session: SessionDep):
    instance = IMGDB(label=label, confidence=confidence, image_url=image_url)
    session.add(instance)
    session.commit()