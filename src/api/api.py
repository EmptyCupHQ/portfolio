from flask import Flask, jsonify, abort
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from pros import pros


api = Flask(__name__)

# extensions
cors = CORS()
cors.init_app(api)

# blueprints
api.register_blueprint(pros)


@api.route('/', methods=['GET'])
def get_routes():
    """
    Fetches list of allowed routes
    """
    routes = {'routes': [(r.rule, r.endpoint)
                         for r in api.url_map.iter_rules() if r.endpoint != 'static']}

    return jsonify(routes)


@api.errorhandler(HTTPException)
def handle_http_error(error):
    """
    Handles all HTTP errors
    """
    # for 500 errors, opaque error message
    if error.code == 500:
        return jsonify({ 'error': 'Something went wrong. Please try again or contact the admin' }), 500

    return jsonify({ 'error': str(error) }), error.code
