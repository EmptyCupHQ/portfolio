from .pros import pros
from flask import Flask, jsonify, abort
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

cors = CORS()

api = Flask(__name__)

cors.init_app(api)

#error handlers
@api.errorhandler(HTTPException)
def http_error(error):
    """
    Handles all HTTP errors
    """
    return jsonify({'error': str(error)}), error.code


api.register_blueprint(pros)


@api.route('/', methods=['GET'])
def get_api_routes():
    """
    Fetches list of allowed routes
    """
    routes = {'routes': [(r.rule, r.endpoint)
                         for r in api.url_map.iter_rules()]}
    if not routes:
        abort(500, description="Could not fetch routes")

    return jsonify(routes), 200
