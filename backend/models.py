from extensions import db  
from datetime import datetime, timezone
import enum


class CargoEnum(enum.Enum):
    ENGENHEIRO_CIVIL = "Engenheiro-civil"
    ENGENHEIRO_SOFTWARE = "Engenheiro-Software"
    ENGENHEIRO_PRODUCAO = "Engenheiro-producao"
    PSICOLOGO = "Psicologo"
    GERENTE_PROJETOS = "Gerente-projetos"

class Usuario(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    nome       = db.Column(db.String(100))
    email      = db.Column(db.String(120), unique=True)
    cargo      = db.Column(db.Enum(CargoEnum), nullable=False)
    senha_hash = db.Column(db.String(200))
    mensagens  = db.relationship("ChatMessage", backref="usuario")

class EspDevice(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    nome     = db.Column(db.String(100))
    token    = db.Column(db.String(200))
    leituras = db.relationship("LeituraESP", backref="device")
    salas    = db.relationship("RoomDevice", backref="device")

class ChatRoom(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    nome       = db.Column(db.String(100))
    mensagens  = db.relationship("ChatMessage", backref="sala")
    devices    = db.relationship("RoomDevice", backref="sala")

class RoomDevice(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    room_id   = db.Column(db.Integer, db.ForeignKey("chat_room.id"))
    device_id = db.Column(db.Integer, db.ForeignKey("esp_device.id"))

class ChatMessage(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    room_id    = db.Column(db.Integer, db.ForeignKey("chat_room.id"))
    user_id    = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    conteudo   = db.Column(db.String(500))
    enviado_em = db.Column(db.DateTime, default=datetime.now(timezone.utc))

class LeituraESP(db.Model):
    id        = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey("esp_device.id"))
    tipo      = db.Column(db.String(50))
    valor     = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))