from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from .config import Config

mongo = PyMongo()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    from .routes import main
    from .auth_route import auth

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(main, url_prefix="/data")

    return app
