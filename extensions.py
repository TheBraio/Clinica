from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
socketio = SocketIO()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")
    migrate.init_app(app, db)

    return app
