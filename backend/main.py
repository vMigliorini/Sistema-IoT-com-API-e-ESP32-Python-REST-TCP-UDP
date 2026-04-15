from flask import Flask
from extensions import db, Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://neondb_owner:npg_nQasPZdpo9A6@ep-odd-scene-acsy6w3o.sa-east-1.aws.neon.tech/neondb?sslmode=require"
bcrypt = Bcrypt(app)

from models import Usuario, EspDevice, ChatRoom, RoomDevice, ChatMessage, LeituraESP

with app.app_context():
    db.create_all()
    print("Tabelas criadas no Neon com sucesso!")

from views import *

if __name__ == "__main__":
    app.run()