from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError
from flask import abort

from config import cloud

blob_service_client = BlobServiceClient(account_url=cloud['blob_store']['account_url'],
                                        credential=cloud['blob_store']['credential_token'])

def upload_blob(blob_name, blob_data, blob_container):
    """
    Uploads the image file to the ABS container
    Returns the url of the image file
    """
    try:
        container_client = blob_service_client.get_container_client(blob_container)
        blob_client = container_client.upload_blob(name=blob_name,data=blob_data)
    except AzureError:
        abort(500, description='Cannot upload image to %s' % (blob_container))

    return blob_client.url


def delete_blob(blob_name, blob_container):
    """
    Deletes the image file from the ABS container
    """
    try:
        container_client = blob_service_client.get_container_client(blob_container)
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.delete_blob()
    except AzureError:
        abort(500, description='Cannot delete image from %s' % (blob_container))