from flask import jsonify


def handle_http_error(error):
    """
    Handles all HTTP errors
    """
    print(error)
    # for 500 errors, opaque error message
    if error.code == 500:
        return jsonify({ 'error': 'Something went wrong. Please try again or contact the admin'}), 500

    return jsonify({ 'error':str(error) }), error.code
