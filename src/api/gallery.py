"""
Gallery Endpoints to Fetch, Upload and Remove image from a pro's gallery
"""

from flask import Blueprint, jsonify, request, abort
import json
import uuid
import datetime
from hashlib import md5
import config
from store import upload_blob, delete_blob
from utils import load_json, save_json, create_thumbnail

gallery = Blueprint('gallery', __name__)

@gallery.route('/<string:pid>/gallery/', methods=['GET'])
def fetch_gallery_details(pid):
    """
    Fetches gallery details of a professional
    """
    # load the database
    try:
        db = load_json(config.DB['JSON_PATH'])
        if not db:
            abort(404, description='No professionals found')
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
        abort(500, description=str(e))

    # check if the pro exists
    if pid not in db:
        abort(404, description='Professional %s not found' % pid)

    return jsonify(db[pid]['gallery'])


@gallery.route('/<string:pid>/gallery/', methods=['POST'])
def upload_gallery(pid):
    """
    Uploads an image to the gallery container and its thumbnail to the thumbnail container of the pro
    """
    # load the database
    try:
        db = load_json(config.DB['JSON_PATH'])
        if not db:
            abort(404, description='No professionals found')
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
        abort(500)

    # check if the pro exists
    if pid not in db:
        abort(404, description='Professional %s not found' % pid)

    # retrieve data from the request
    image = request.files['image']
    description = request.form['description'] if 'description' in request.form else None

    # upload the image to the blob store
    image_details = {}
    image_id = md5(str(uuid.uuid4()).encode('utf-8')).hexdigest()[:16]
    image_details['id'] = image_id

    try:
        image_url = upload_blob(image_id, image, config.BLOB_STORE['GALLERY_CONTAINER'])
    except Exception:
        abort(500, description='Failed to upload image to blob store')
    image_details['ref'] = image_url

    # create a thumbnail of the image
    thumbnail = create_thumbnail(image, config.GALLERY['THUMBNAIL_RESOLUTION'])
    try:
        thumbnail_url = upload_blob(image_id, thumbnail, config.BLOB_STORE['THUMBNAIL_CONTAINER'])
    except Exception as e:
        abort(500, description='Failed to upload thumbnail to blob store')
    image_details['thumbnail_ref'] = thumbnail_url

    image_details['description'] = description
    image_details['uploaded_at'] = datetime.datetime.now().timestamp()

    # add the image details to the professional's gallery
    db[pid]['gallery'].append(image_details)

    try:
        save_json(config.DB['JSON_PATH'], db)
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
        abort(500)
    
    return jsonify({ 'message': 'Successfully uploaded image to %s gallery' % (pid) }), 201


@gallery.route('/<string:pid>/gallery/<string:imgid>/', methods=['DELETE'])
def delete_gallery(pid, imgid):
    """
    Removes an image from the gallery
    """
    # load the database
    try:
        db = load_json(config.DB['JSON_PATH'])
        if not db:
            abort(404, description='No professionals found')
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
        abort(500)

    # check if the pro exists   
    if pid not in db:
        abort(404, description='Professional %s not found' % pid)

    # check if the image exists in the gallery of the pro
    for img in db[pid]['gallery']:
        if img['id'] == imgid: 
            # delete the image from the blob store      
            try:
                delete_blob(imgid, config.BLOB_STORE['GALLERY_CONTAINER'])
                delete_blob(imgid, config.BLOB_STORE['THUMBNAIL_CONTAINER'])
            except Exception as e:
                abort(500, description=str(e))
            
            # remove the image from the gallery of the pro
            db[pid]['gallery'].remove(img)

            # save the database
            try:
                save_json(config.DB['JSON_PATH'], db)
            except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
                abort(500)
            return jsonify({ 'message': 'Successfully removed image %s from %s gallery' % (imgid, pid) }), 200
    
    abort(404, description='Image %s not found in %s gallery' % (imgid, pid))
