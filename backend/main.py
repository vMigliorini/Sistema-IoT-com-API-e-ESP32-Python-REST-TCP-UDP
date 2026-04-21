from flask import Flask
from flask_cors import CORS
from extensions import db, bcrypt, socketio
from views import views_bp
import os


app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'chave-so-pra-dev')

socketio.init_app(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://neondb_owner:npg_nQasPZdpo9A6@ep-odd-scene-acsy6w3o.sa-east-1.aws.neon.tech/neondb?sslmode=require"

CORS(app, supports_credentials=True, origins=["http://localhost:5000","http://127.0.0.1:5000"])

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(views_bp)


with app.app_context():
    from models import Usuario, EspDevice, ChatRoom, RoomDevice, ChatMessage, LeituraESP
    db.create_all()


if __name__ == "__main__":
    socketio.run(app, debug=True)