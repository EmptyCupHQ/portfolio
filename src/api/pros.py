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
    db = load_json('./src/api/db.json')
    if not db:
        abort(500)

    return jsonify(db), 200


@pros.route('/', methods=['POST'])
def create_pro():
    """
    Adds a new professional to directory
    """
    data = request.get_json()
    if not data:
        abort(400)

    uid = uuid.uuid1()
    if not uid:
        abort(500)
    try:
        pros = {
            'uid': str(uid),
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
        abort(400, description="{} is missing".format(e))

    db = load_json('./src/api/db.json')

    if not db:
        abort(500)
    db[str(uid)] = pros

    if save_json('./src/api/db.json', db):
        return jsonify({ 'message': 'Successfully registered User with {}'.format(str(uid)) }), 201
    
    abort(500)

@pros.route('/<string:pid>', methods=['GET'])
def get_pro(pid):
    """
    Gets a profile data for professional by id `pid`
    """
    db = load_json('./src/api/db.json')
    if not db:
        abort(500)

    if pid in db:
        return jsonify(db[pid]), 200

    return abort(404, description="No such professional {}".format(pid))


@pros.route('/<string:pid>', methods=['PATCH'])
def update_pro(pid):
    """
    Updates a profile data for professional by id `pid`
    """
    data = request.get_json()
    if not data:
        abort(400)

    db = load_json('./src/api/db.json')

    if pid not in db:
        return abort(404, description="No such professional {}".format(pid))
    for (key, value) in data.items():
        if key in db[pid] and key not in ['uid', 'active']:
            db[pid][key] = value
        else:
            return abort(404, description="'{}' is not an existing field".format(key))
    db[pid]['active'] = datetime.datetime.utcnow().timestamp()

    if save_json('./src/api/db.json', db):
        return jsonify({ 'message': 'Successfully updated fields {} of user with pid {}'.format([k for k in data.keys()], pid) }), 200

    abort(500)