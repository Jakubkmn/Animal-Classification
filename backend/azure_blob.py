from azure.storage.blob import BlobServiceClient
import base64
from dotenv import load_dotenv
import uuid
import os

load_dotenv()

connection_str = os.environ["AZURE_CONNECTION_STR"]
container_name = os.environ["AZURE_CONTAINER_NAME"]

blob_service_client = BlobServiceClient.from_connection_string(connection_str)


def upload_to_azure(file_name, image_bytes):
    unique_filename = f"{uuid.uuid4()}_{file_name}"
    container_client = blob_service_client.get_container_client(container=container_name)
    blob_client = container_client.get_blob_client(blob=unique_filename)
    blob_client.upload_blob(image_bytes, overwrite=False)
    return blob_client.url, blob_client.blob_name

def download_from_azure(image_url):
    container_client = blob_service_client.get_container_client(container=container_name)
    blob_client = container_client.get_blob_client(blob=image_url)
    data = blob_client.download_blob().readall()
    return data

def get_all_images():
    container_client = blob_service_client.get_container_client(container=container_name)

    images = []
    for blob in container_client.list_blobs():
        blob_client = container_client.get_blob_client(blob.name)
        blob_data = blob_client.download_blob().readall()
        base64_image = base64.b64encode(blob_data).decode("utf-8")
        images.append({
            "blob_name": blob.name,
            "data": f"data:image/jped;base64,{base64_image}"
        })
    return images