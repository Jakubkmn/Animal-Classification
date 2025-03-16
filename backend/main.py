from fastapi import FastAPI, UploadFile, Depends
from fastapi.responses import RedirectResponse
from sqlmodel import Field, Session, SQLModel, create_engine, TIMESTAMP
from datetime import datetime
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
    classification_result : str = Field(default=None)
    pred_prob : float = Field(default=None)
    timestamps : datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))
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
async def predict(file: UploadFile):
    contents = await file.read() # Returns bytes
    img = Image.open(io.BytesIO(contents)).convert('RGB')
    img = img.resize((128,128))
    image_array = np.array(img)
    image_array = np.expand_dims(image_array, axis=0)

    prediction = model.predict(image_array)

    label = "dog" if prediction[0][0] > 0.5 else "cat"
    return {"prediction": label, "confidence": float(prediction[0][0])}