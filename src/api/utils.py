import io
from PIL import Image
import json


def load_json(filep):
    """
    Reads from JSON file and returns data.
    """
    with open(filep, 'r') as rf:
        data = json.load(rf)
        return data 


def save_json(filep, data):
    """
    Writes to a JSON file.
    """
    with open(filep, 'w') as wf:
        json.dump(data, wf)


def create_thumbnail(image, resolution):
    """
    Input is a FileObject.
    Creates and returns thumbnail of the image of the resolution.
    """
    image = Image.open(image)
    image.thumbnail(resolution)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)
    return image_bytes
