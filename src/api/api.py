import os
import sys

# add config module to path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
)

from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

import controller
import errors


api = Flask(__name__)

# extensions
cors = CORS()
cors.init_app(api)


api.add_url_rule('/', 'get_routes', controller.get_routes, methods=['GET'])

api.add_url_rule('/pros/', 'list_pros', controller.list_pros, methods=['GET'])
api.add_url_rule('/pros/', 'create_pro', controller.create_pro, methods=['POST'])
api.add_url_rule('/pros/<string:pid>', 'get_pro', controller.get_pro, methods=['GET'])
api.add_url_rule('/pros/<string:pid>', 'update_pro', controller.update_pro, methods=['PATCH'])

api.add_url_rule('/pros/<string:pid>/gallery/', 'get_gallery', controller.get_gallery, methods=['GET'])
api.add_url_rule('/pros/<string:pid>/gallery/', 'upload_gallery', controller.upload_gallery, methods=['POST'])
api.add_url_rule('/pros/<string:pid>/gallery/<string:imgid>', 'del_gallery_img', controller.del_gallery_img, methods=['DELETE'])

# error handlers
api.register_error_handler(HTTPException, errors.handle_http_error)
