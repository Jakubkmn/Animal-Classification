FROM python:3.12.9-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

COPY my_model.keras /app/my_model.keras

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]