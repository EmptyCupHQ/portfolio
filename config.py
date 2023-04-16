import os

from azure.identity import DefaultAzureCredential

# azure settings
BLOB_STORE = {
    "CREDENTIAL_TOKEN": DefaultAzureCredential(),
    "GALLERY_CONTAINER": os.getenv("GALLERY_CONTAINER"),
    "THUMBNAIL_CONTAINER": os.getenv("THUMBNAIL_CONTAINER"),
    "ACCOUNT_URL": os.getenv("BLOB_STORE_ACCOUNT_URL")
}

# database settings
DB = {
    "JSON_PATH": os.getenv("DB_JSON_PATH")
}

# gallery settings
GALLERY = {
    "THUMBNAIL_RESOLUTION": tuple(map(int, os.getenv("THUMBNAIL_RESOLUTION").split("x"))) if "THUMBNAIL_RESOLUTION" in os.environ else None
    or (256, 144)  # default resolution YouTube 144p
}
