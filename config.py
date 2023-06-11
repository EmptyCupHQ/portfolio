import os

from azure.identity import DefaultAzureCredential

# azure settings
cloud = {
    'blob_store': {
        'credential_token': DefaultAzureCredential(),
        'gallery': os.getenv('GALLERY'),
        'thumbnail': os.getenv('THUMBNAIL'),
        'account_url': os.getenv('BLOB_STORE_ACCOUNT_URL')
    }
}

# database settings
DB = {
    'json_path': os.getenv('DB_JSON_PATH')
}

# gallery settings
GALLERY = {
    'thumbnail_res': tuple(map(int, os.getenv('THUMBNAIL_RES').split('x'))) if 'THUMBNAIL_RES' in os.environ 
                                                                            else (256, 144)  # default resolution YouTube 144p
}
