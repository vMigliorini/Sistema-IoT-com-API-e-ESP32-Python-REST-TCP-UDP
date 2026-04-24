from extensions import socketio
from models import Usuario, CargoEnum, EspDevice, ChatRoom, RoomDevice, ChatMessage, LeituraESP, UsuarioChat, StatusConexaoEnum
from flask import session
from sqlalchemy import select, func, update, delete
from flask_socketio import send, emit, join_room, leave_room, disconnect
from services.socket_service import entrar_sala, atualizar_desconexao
from functools import wraps



def socket_login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            emit("message", {"username": "Sistema", "data": "Sessão expirada"})
            disconnect()
            return
        return f(*args, **kwargs)
    return decorated




#socketIO
@socketio.on('connect')
def handle_connect():
    pass

@socketio.on('join')
@socket_login_required
def handle_join(room_id):

    user_id = session.get("user_id")

    _, erro = entrar_sala(room_id, user_id)

    if erro:
        emit("message", {"username": "Sistema", "data": erro})
        return

    session['room_id'] = room_id
    join_room(room_id)

    username = session.get("username")
    chat = session.get("room_name")
    emit("message", {"username": "Sistema", "data": f"{username} entrou em #{chat}"}, to=room_id)

@socketio.on('message')
@socket_login_required
def handle_message(data):
    username = session.get('username', 'Anônimo')
    room_id = session.get('room_id')
    emit("message", {"username": username, "data": data}, to=room_id)


@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    user_id = session.get('user_id')
    room_id = session.get('room_id')

    _, erro = atualizar_desconexao(user_id)

    if erro:
        emit("message", {"username": "Sistema", "data": erro})
        return

    emit("message", {"username": "Sistema", "data": f"{username} saiu do chat"}, to=room_id)


