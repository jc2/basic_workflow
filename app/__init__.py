import os

from flask import Flask
from flask_mongoengine import MongoEngine

db = MongoEngine()


def init_app():
    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {
        'host': os.getenv('MONGO_HOST'),
        'port': int(os.getenv('MONGO_PORT')),
        'db': os.getenv('MONGO_DB'),
        'username': os.getenv('MONGO_USER'),
        'password': os.getenv('MONGO_PASSWORD')
    }

    db.init_app(app)

    with app.app_context():
        from .api import bp
        app.register_blueprint(bp)
        return app
