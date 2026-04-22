from extensions import bcrypt, db, socketio
from models import Usuario, CargoEnum, EspDevice, ChatRoom, RoomDevice, ChatMessage, LeituraESP, UsuarioChat, StatusConexaoEnum
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import send, emit, join_room, leave_room
from sqlalchemy import select, func, update, delete


views_bp = Blueprint('views', __name__)





#socketIO
@socketio.on('connect')
def handle_connect():
    pass

@socketio.on('join')
def handle_join(room_id):
    username = session.get('username')
    user_id = session.get('user_id')

    sala = db.session.get(ChatRoom, room_id)
    if not sala:
        emit("message", {"data": "Sala não encontrada"})
        return

    session['room_id'] = room_id

    stmt = select(UsuarioChat).where(UsuarioChat.id_usuario == user_id, UsuarioChat.room_id == room_id)
    membro = db.session.execute(stmt).scalar()

    if membro:
        membro.status = StatusConexaoEnum.conectado
    else:
        membro = UsuarioChat(id_usuario=user_id, room_id=room_id)
        db.session.add(membro)

    db.session.commit()
    join_room(room_id)
    emit("message", {"username": "Sistema", "data": f"{username} entrou no chat"}, to=room_id)

@socketio.on('message')
def handle_message(data):
    username = session.get('username', 'Anônimo')
    room_id = session.get('room_id')
    emit("message", {"username": username, "data": data}, to=room_id)

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    user_id = session.get('user_id')
    room_id = session.get('room_id')
    stmt = (
            update(UsuarioChat)
            .where(UsuarioChat.id_usuario == user_id)
            .values(status=StatusConexaoEnum.desconectado)
        )
    db.session.execute(stmt)
    db.session.commit()

    emit("message", {"username": "Sistema", "data": f"{username} saiu do chat"}, to=room_id)





#rotas
@views_bp.route("/chat_rooms", methods=["GET", "POST"])
def chat_rooms():
    if request.method == "GET":
        if 'user_id' not in session:
            return redirect(url_for('views.login'))
        
        return render_template("chat_rooms.html")

    
    dados_nova_sala = request.json
    nome_sala = dados_nova_sala["nome_sala"]

    stmt = select(ChatRoom).where(ChatRoom.nome == nome_sala)
    sala = db.session.execute(stmt).scalar()
    if sala:
        return jsonify({"ok": False, "erro": "Erro! Esse nome de sala já existe!"})

    novo = ChatRoom(nome=nome_sala)
    db.session.add(novo)
    db.session.commit()

    membro = UsuarioChat(id_usuario=session['user_id'], room_id=novo.id)
    db.session.add(membro)
    db.session.commit()

    return jsonify({"ok": True, "nome": novo.nome, "room_id": novo.id})


@views_bp.route("/chat_rooms/listar", methods=["GET"])
def listar_chat_rooms():
    if 'user_id' not in session:
        return jsonify({"ok": False}), 401
    
    rooms_vazias = [
        row.id for row in (
            db.session.query(ChatRoom.id)
            .outerjoin(UsuarioChat, (UsuarioChat.room_id == ChatRoom.id) &
                                    (UsuarioChat.status == StatusConexaoEnum.conectado))
            .group_by(ChatRoom.id)
            .having(func.count(UsuarioChat.id_usuario) == 0)
            .all()
        )
    ]

    if rooms_vazias:
        db.session.execute(delete(UsuarioChat).where(UsuarioChat.room_id.in_(rooms_vazias)))
        db.session.execute(delete(ChatRoom).where(ChatRoom.id.in_(rooms_vazias)))
        db.session.commit()

    contagens = (
        db.session.query(ChatRoom.id, ChatRoom.nome, func.count(UsuarioChat.id_usuario))
        .outerjoin(UsuarioChat, UsuarioChat.room_id == ChatRoom.id)
        .filter(
            (UsuarioChat.status == StatusConexaoEnum.conectado) | 
            (UsuarioChat.status == None)
        )
        .group_by(ChatRoom.id)
        .all()
    )
    return jsonify([{"id_sala": id_sala, "nome": nome, "usuarios": qtd} for id_sala, nome, qtd in contagens])

@views_bp.route("/chat_rooms/listar_nome_users", methods=["GET"])
def listar_nome_users():

    room_id_str = request.args.get('room_id')

    room_id = int(room_id_str)

    resultados = (
        db.session.query(Usuario.nome)
        .join(UsuarioChat, Usuario.id == UsuarioChat.id_usuario)
        .filter(
            UsuarioChat.status == StatusConexaoEnum.conectado,
            UsuarioChat.room_id == room_id
        )
        .all()
    )

    lista_de_nomes = [usuario[0] for usuario in resultados]

    return jsonify({"ok": True, "usuarios": lista_de_nomes})

@views_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    dados_login = request.json
    email =  dados_login["email"]
    senha = dados_login["senha"]

    stmt = select(Usuario).where(Usuario.email == email)
    usuario = db.session.execute(stmt).scalar()

    if not usuario:
        return jsonify({"ok": False, "erro": "Email não cadastrado"}), 400
    

    senha_valida = bcrypt.check_password_hash(usuario.senha_hash, senha)

    if senha_valida:
        session['user_id'] = usuario.id
        session['username'] = usuario.nome
        session['role'] = usuario.cargo.value
        return jsonify({"ok": True, "redirect": url_for('views.chat_rooms')})
    else:
        return jsonify({"ok": False, "erro": "Senha inválida"}), 400
    

@views_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")
    
    dados_cadastro = request.json
    nome = dados_cadastro["nome"]
    email = dados_cadastro["email"]
    senha = dados_cadastro["senha"]
    cargo = dados_cadastro["cargo"]
    try:
        cargo_enum = CargoEnum(cargo)
    except ValueError:
        return jsonify({"ok": False, "erro": "Cargo inválido"}), 400

    stmt = select(Usuario).where(Usuario.email == email)
    usuario_existente = db.session.execute(stmt).scalar()
    if usuario_existente:
        return jsonify({"ok": False, "erro": "E-mail já cadastrado"}), 400

    hash_senha = bcrypt.generate_password_hash(senha).decode("utf-8")
    novo = Usuario(nome=nome, email=email, cargo=cargo_enum, senha_hash=hash_senha)
    db.session.add(novo)
    db.session.commit()

    return jsonify({"ok": True, "redirect": url_for('views.login')}), 201

@views_bp.route("/me")
def me():
    if 'user_id' not in session:
        return jsonify({"ok": False}), 401
    else:
        return jsonify({
            "ok": True,
            "id": session['user_id'],
            "nome": session['username'],
            "cargo": session['role']
        })
    