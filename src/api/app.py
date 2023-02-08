from flask import Flask
from flask_cors import CORS

cors = CORS()


def create_app():

    app = Flask(__name__)

    app.config['TESTING'] = True
    cors.init_app(app)

    from .main import main
    app.register_blueprint(main)
    from .pros import pros
    app.register_blueprint(pros)

    return app
