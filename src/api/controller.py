import datetime
import uuid

from flask import jsonify, request, abort, current_app as api

from config import cloud, GALLERY
import db
import store
import utils


def get_routes():
    """
    Fetches list of allowed routes
    """
    routes = {'routes': [(r.rule, r.endpoint)
                         for r in api.url_map.iter_rules() if r.endpoint != 'static']}

    return jsonify(routes)


def list_pros():
    """
    Fetches list of professionals
    """
    daba = db.load()
    return jsonify(daba)


def create_pro():
    """
    Adds a new professional to directory
    """
    data = request.get_json()
    if not data:
        abort(400, description='Empty request data')

    uid = str(uuid.uuid1())
    try:
        pros = {
            'uid': uid,
            'type': data['type'],
            'firstname': data['firstname'],
            'lastname': data['lastname'],
            'about': data['about'],
            'active': datetime.datetime.utcnow().timestamp(),
            'bio': data['bio'],
            'email': data['email'],
            'contact': data['contact'],
            'whatsapp': data['whatsapp'] if 'whatsapp' in data else True,
            'gallery': []
        }
    except KeyError as e:
        abort(400, description="%s is missing" % e)

    daba = db.load()

    daba[uid] = pros

    db.save(daba)

    return jsonify({ 'message': 'Successfully registered User with %s' % uid }), 201


@db.if_pro_exists
def get_pro(pid):
    """
    Gets a profile data for professional by id `pid`
    """

    daba = db.load()

    return jsonify(daba[pid])


@db.if_pro_exists
def update_pro(pid):
    """
    Updates a profile data for professional by id `pid`
    """
    data = request.get_json()
    if not data:
        abort(400, description='Empty request data')

    daba = db.load()

    for (key, value) in data.items():
        if key in daba[pid] and key not in ['uid', 'active', 'gallery']:
            daba[pid][key] = value
        else:
            return abort(404, description="'%s' is not an existing field" % key)
    daba[pid]['active'] = datetime.datetime.utcnow().timestamp()

    db.save(daba)

    return jsonify({'message': 'Successfully updated field(s) (%s) of user %s'
                    % (', '.join(data.keys()), pid)})


@db.if_pro_exists
def get_gallery(pid):
    """
    Fetches gallery details of a professional
    """  
    daba = db.load()   
    return jsonify(daba[pid]['gallery'])


@db.if_pro_exists
def upload_gallery(pid):
    """
    Uploads an image to the gallery container and its thumbnail to the thumbnail container of the pro
    """

    daba = db.load()

    imgf = request.files.get('image')
    if imgf is None:
        abort(400, description='No image found in request')
    desc = request.form.get('description')

    img = {}
    img_id = utils.generate_uuid()
    img['id'] = img_id

    img_url = store.upload_blob(img_id, imgf, cloud['blob_store']['gallery'])
    img['ref'] = img_url

    thumnlf = utils.create_thumbnail(imgf, GALLERY['thumbnail_res'])
    thumnl_url = store.upload_blob(img_id, thumnlf, cloud['blob_store']['thumbnail'])
    img['thumbnail_ref'] = thumnl_url

    img['description'] = desc
    img['uploaded_at'] = datetime.datetime.now().timestamp()

    # add the image details to the professional's gallery
    daba[pid]['gallery'].append(img)

    db.save(daba)
    
    return jsonify({ 'message': 'Successfully uploaded image to %s\'s gallery' % (pid) }), 201


@db.if_pro_exists
def del_gallery_img(pid, imgid):
    """
    Removes an image from the gallery
    """
    daba = db.load()

    # check if the image exists in the gallery of the pro
    for img in daba[pid]['gallery']:
        if img['id'] == imgid: 
            # delete the image from the blob store      
            store.delete_blob(imgid, cloud['blob_store']['gallery'])
            store.delete_blob(imgid, cloud['blob_store']['thumbnail'])
            
            daba[pid]['gallery'].remove(img)

            db.save(daba)
            return jsonify({ 'message': 'Successfully removed image: %s from %s\'s gallery' % (imgid, pid) }), 200
    
    abort(404, description='Image %s not found in %s gallery' % (imgid, pid))
