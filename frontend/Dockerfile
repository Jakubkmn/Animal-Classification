FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run" "main:app", "--server.port=8501", "--server.address=0.0.0.0"]