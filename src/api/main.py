from flask import Blueprint, make_response, jsonify, current_app as app

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    """
    Fetches list of allowed routes
    """
    try:
        routes = { 'routes': [(r.rule,r.endpoint) for r in app.url_map.iter_rules()] }
    except Exception as e:
        responseObject = {
            'status': 'FAIL',
            'message': 'Could not fetch routes'
        }
        return make_response(jsonify(responseObject), 500)

    #print(routes)
    return make_response(jsonify(routes),200)