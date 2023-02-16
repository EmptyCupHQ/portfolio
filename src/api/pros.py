from flask import Blueprint, jsonify, request, abort
import uuid
import datetime
import json
from utils import load_json, save_json

pros = Blueprint('pros', __name__, url_prefix='/pros')


@pros.route('/', methods=['GET'])
def list_pros():
    """
    Fetches list of professionals
    """
    try:
        db = load_json('./src/api/db.json')
        if not db:
            abort(404, description='No professionals found')
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
        abort(500)

    return jsonify(db)


@pros.route('/', methods=['POST'])
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
            'whatsapp': data['whatsapp'] if 'whatsapp' in data else True
        }
    except KeyError as e:
        abort(400, description="%s is missing"%e)

    try:
        db = load_json('./src/api/db.json')
        if not db:
            abort(404, description='No professionals found')
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
        abort(500)

    db[uid] = pros

    try:
        save_json('./src/api/db.json', db)
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
        abort(500)
    
    return jsonify({ 'message': 'Successfully registered User with %s'%uid }), 201
    
    

@pros.route('/<string:pid>', methods=['GET'])
def get_pro(pid):
    """
    Gets a profile data for professional by id `pid`
    """
    try:
        db = load_json('./src/api/db.json')
        if not db:
            abort(404, description='No professionals found')
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
        abort(500)

    if pid in db:
        return jsonify(db[pid])

    return abort(404, description="No such professional %s"%pid)


@pros.route('/<string:pid>', methods=['PATCH'])
def update_pro(pid):
    """
    Updates a profile data for professional by id `pid`
    """
    data = request.get_json()
    if not data:
        abort(400, description='Empty request data')

    try:
        db = load_json('./src/api/db.json')
        if not db:
            abort(404, description='No professionals found')
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
        abort(500)

    if pid not in db:
        return abort(404, description="No such professional %s"%pid)
    for (key, value) in data.items():
        if key in db[pid] and key not in ['uid', 'active']:
            db[pid][key] = value
        else:
            return abort(404, description="'%s' is not an existing field" % key)
    db[pid]['active'] = datetime.datetime.utcnow().timestamp()

    try:
        save_json('./src/api/db.json', db)
    except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
        abort(500)

    return jsonify({ 'message': 'Successfully updated fields %s of user with pid %s'
                        % (data.keys(), pid) })