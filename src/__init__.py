from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()


def init_app(testing=False):
    app = Flask(__name__, instance_relative_config=False)
    load_dotenv()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DB_URI')
        app.config['TESTING'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')

    db.init_app(app)

    with app.app_context():
        from . import routes

        return app
