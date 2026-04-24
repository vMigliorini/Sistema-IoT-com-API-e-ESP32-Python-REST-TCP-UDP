from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO

db = SQLAlchemy()
bcrypt = Bcrypt()
socketio = SocketIO(async_mode='threading', cors_allowed_origins="*")