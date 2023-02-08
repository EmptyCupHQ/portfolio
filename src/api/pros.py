from flask import Blueprint, jsonify, make_response, request, current_app as app
from .models import Professional
import uuid
import datetime
import json

pros = Blueprint('pros', __name__, url_prefix='/pros')


@pros.route('/', methods=['GET'])
def listProfessionals():
    """
    Fetches list of professionals
    """
    try:
        with open('db.json', 'r') as rf:
            data = json.load(rf)
    except Exception as e:
        responseObject = {
            'status': 'FAIL',
            'message': str(e)
        }
        return make_response(jsonify(responseObject), 500)

    return make_response(jsonify(data), 200)


@pros.route('/', methods=['POST'])
def createProfessional():
    """
    Adds a new professional to directory
    """
    try:
        data = request.get_json()
        uid = str(uuid.uuid1())
        pros = {
            'uid': uid,
            'type': data['type'],
            'firstName': data['firstName'],
            'lastName': data['lastName'],
            'about': data['about'],
            'active': datetime.datetime.utcnow().timestamp(),
            'bio': data['bio'],
            'email': data['email'],
            'contact': data['contact'],
            'whatsapp': data['whatsapp'],
        }
    except Exception as e:
        responseObject = {
            'status': 'FAIL',
            'message': str(e)
        }
        return make_response(jsonify(responseObject), 400)

    try:
        with open('db.json', 'r') as rf:
            db = json.load(rf)
    except Exception as e:
        responseObject = {
            'status': 'FAIL',
            'message': str(e)
        }
        return make_response(jsonify(responseObject), 500)

    db[uid] = pros
    #print(db[uid])

    try:
        with open('db.json', 'w') as wf:
            json.dump(db, wf)
    except Exception as e:
        responseObject = {
            'status': 'fail',
            'message': str(e)
        }
        return make_response(jsonify(responseObject), 500)

    return make_response(jsonify({'status': 'SUCCESS',
                                  'message': 'Successfully registered'}), 201)


@pros.route('/<string:pid>', methods=['GET'])
def getProfessional(pid):
    """
    Gets a profile data for professional by id `pid`
    """

    try:
        with open('db.json', 'r') as rf:
            db = json.load(rf)
    except Exception as e:
        responseObject = {
            'status': 'FAIL',
            'message': str(e)
        }
        return make_response(jsonify(responseObject), 500)

    if pid in db:
        return make_response(jsonify(db[pid]), 200)
    else:
        responseObject = {
            'status': 'FAIL',
            'message': 'No such professional'
        }
        return make_response(jsonify(responseObject), 404)


@pros.route('/<string:pid>', methods=['PUT'])
def updateProfessional(pid):

    try:
        data = request.get_json()
        with open('db.json', 'r') as rf:
            db = json.load(rf)
    except Exception as e:
        responseObject = {
            'status': 'FAIL',
            'message': str(e)
        }
        return make_response(jsonify(responseObject), 500)

    if pid in db:
        db[pid]['type'] = data['type']
        db[pid]['firstName'] = data['firstName']
        db[pid]['lastName'] = data['lastName']
        db[pid]['about'] = data['about']
        db[pid]['active'] = datetime.datetime.utcnow().timestamp()
        db[pid]['bio'] = data['bio']
        db[pid]['email'] = data['email']
        db[pid]['contact'] = data['contact']
        db[pid]['whatsapp'] = data['whatsapp']
        try:
            with open('db.json', 'w') as wf:
                json.dump(db, wf)
        except Exception as e:
            responseObject = {
                'status': 'FAIL',
                'message': str(e)
            }
            return make_response(jsonify(responseObject), 500)
        return make_response(jsonify({'status': 'SUCCESS',
                                      'message': 'Successfully updated'}), 200)
    else:
        responseObject = {
            'status': 'FAIL',
            'message': 'No such professional'
        }
        return make_response(jsonify(responseObject), 404)
