from flask import Blueprint, jsonify, request, abort
import uuid
import datetime
import json
from .utils import read_db, write_db

pros = Blueprint('pros', __name__, url_prefix='/pros')


@pros.route('/', methods=['GET'])
def list_pros():
    """
    Fetches list of professionals
    """
    db = read_db('db.json')
    return jsonify(db), 200


@pros.route('/', methods=['POST'])
def create_profile():
    """
    Adds a new professional to directory
    """
    data = request.get_json()
    if not data:
        abort(400)
    uid = str(uuid.uuid1())
    if not uid:
        abort(500, description="Could not generate uid")
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
            'whatsapp': data['whatsapp'] if data.get('whatsapp') else True
        }
    except KeyError as e:
        abort(400, description="{} is missing".format(e))
    db = read_db('db.json')
    db[uid] = pros
    write_db('db.json', db)
    return jsonify({'pid': uid, 'message': 'Successfully Registered User'}), 201


@pros.route('/<string:pid>', methods=['GET'])
def get_profile(pid):
    """
    Gets a profile data for professional by id `pid`
    """
    db = read_db('db.json')
    if pid in db:
        return jsonify(db[pid]), 200
    return abort(404, description="No such professional")


@pros.route('/<string:pid>', methods=['PATCH'])
def update_profile(pid):
    """
    Updates a profile data for professional by id `pid`
    """
    data = request.get_json()
    if not data:
        abort(400)
    db = read_db('db.json')
    if pid not in db:
        return abort(404, description="No such professional")
    for (key, value) in data.items():
        if key in db[pid] and key not in ['uid', 'active']:
            db[pid][key] = value
        else:
            return abort(404, description="'{}' is not an existing field".format(key))
    db[pid]['active'] = datetime.datetime.utcnow().timestamp()
    write_db('db.json', db)
    return jsonify({'pid': pid, 'message': 'Successfully Updated User: {}'.format([k for k in data.keys()])}), 200
