from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, socketio
from views import views_bp
from dotenv import load_dotenv
import os

load_dotenv()

NEON_DB_URI = os.getenv("NEON_DB_URI")

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY')

socketio.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = NEON_DB_URI

CORS(app, origins=[os.getenv("FRONTEND_URL")])

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(views_bp)

import socket_events

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    socketio.run(app, debug=True)