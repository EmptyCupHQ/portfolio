"""
Functions to upload and delete files from the Azure Blob Storage
"""

from azure.storage.blob import BlobServiceClient
from config import BLOB_STORE

blob_service_client = BlobServiceClient(account_url=BLOB_STORE['ACCOUNT_URL'], credential=BLOB_STORE['CREDENTIAL_TOKEN'])

def upload_blob(blob_name, blob_data, blob_container):
    """
    Uploads the image file to the ABS container
    Returns the url of the image file
    """
    container_client = blob_service_client.get_container_client(blob_container)
    blob_client = container_client.upload_blob(name=blob_name,data=blob_data)
    return blob_client.url


def delete_blob(blob_name, blob_container):
    """
    Deletes the image file from the ABS container
    """
    container_client = blob_service_client.get_container_client(blob_container)
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.delete_blob()