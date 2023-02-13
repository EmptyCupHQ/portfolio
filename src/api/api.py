from pros import pros
from flask import Flask, jsonify, abort
from werkzeug.exceptions import HTTPException
from flask_cors import CORS


api = Flask(__name__)

cors = CORS()
cors.init_app(api)


@api.errorhandler(HTTPException)
def handle_http_error(error):
    """
    Handles all HTTP errors
    """
    # for 500 errors, opaque error message
    if error.code == 500:
        return jsonify({ 'error': 'Something went wrong. Please try again or contact the admin' }), 500
    
    return jsonify({ 'error': str(error) }), error.code


api.register_blueprint(pros)


@api.route('/', methods=['GET'])
def get_routes():
    """
    Fetches list of allowed routes
    """
    routes = { 'routes': [(r.rule, r.endpoint)
                         for r in api.url_map.iter_rules()] }
    if not routes:
        abort(500)

    return jsonify(routes), 200
