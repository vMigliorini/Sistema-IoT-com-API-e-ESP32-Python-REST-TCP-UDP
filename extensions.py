from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
origens_permitidas = os.getenv("FRONTEND_URL", "*")
socketio = SocketIO(async_mode='threading', cors_allowed_origins=origens_permitidas)