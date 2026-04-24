from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from sqlalchemy import select, func, update, delete
from functools import wraps
from services.chat_service import listar_nome_users, listar_salas, limpar_salas_vazias, criar_sala
from services.auth_service import cadastrar, logar

views_bp = Blueprint('views', __name__)


#confirmação de login
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({"ok": False, "erro": "Não autenticado"}), 401
            return redirect(url_for('views.login'))
        return f(*args, **kwargs)
    return decorated


#rotas salas de chat

@views_bp.route("/chat_rooms", methods=["GET"])
@login_required
def chat_rooms(): 
    return render_template("chat_rooms.html")



@views_bp.route("/api/chat_rooms", methods=["POST"])
@login_required
def criar_chat_room():
    nome_sala = request.json.get("nome_sala")
    sala, erro = criar_sala(nome_sala, session['user_id'])
    if erro:
        return jsonify({"ok": False, "erro": erro}), 400
    session["room_name"] = sala.nome
    return jsonify({"ok": True, "nome": sala.nome, "room_id": sala.id})




@views_bp.route("/api/chat_rooms", methods=["GET"])
@login_required
def listar_chat_rooms():
    salas, erro = listar_salas()
    if erro:
        return jsonify({"erro": erro})
    return jsonify([{"id_sala": id, "nome": nome, "usuarios": qtd} for id, nome, qtd in salas])



@views_bp.route("/api/chat_rooms/<int:room_id>", methods=["GET"])
@login_required
def listar_usuarios_chat_room(room_id):
    usuarios, erro = listar_nome_users(room_id)
    if erro:
        return jsonify({"ok": False, "Erro": erro})
    return jsonify({"ok": True, "usuarios": usuarios})



@views_bp.route("/api/chat_rooms", methods=["DELETE"])
@login_required
def limpar_chat_rooms():
    erro = limpar_salas_vazias()
    if erro:
        return jsonify({"ok": False, "erro": erro})
    return jsonify({"ok": True})





#rotas login
@views_bp.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@views_bp.route("/api/login", methods=["POST"])
def fazer_login():
    dados_login = request.json
    email =  dados_login.get("email")
    senha = dados_login.get("senha")
    login, erro = logar(email, senha)

    if erro:
        return jsonify({"ok": False, "erro": erro})
    
    session['user_id'] = login.get("id")
    session['username'] = login.get("nome")
    session['role'] = login.get("cargo")

    return jsonify({"ok": True, "redirect": url_for('views.chat_rooms')})






#rotas cadastro
@views_bp.route("/cadastro", methods=["GET"])
def cadastro():
    return render_template("cadastro.html")

@views_bp.route("/api/cadastro",  methods=["POST"])
def fazer_cadastro():
    dados_cadastro = request.json
    nome = dados_cadastro.get("nome")
    email = dados_cadastro.get("email")
    senha = dados_cadastro.get("senha")
    cargo = dados_cadastro.get("cargo")

    cadastro, erro = cadastrar(nome, email, senha, cargo)

    if erro:
        return jsonify({"ok": False, "erro": erro})
    
    if cadastro:
        return jsonify({"ok": True, "redirect": url_for('views.login')})
    

    
#rota para pegar dados
@views_bp.route("/me")
@login_required
def me():
    return jsonify({
        "ok": True,
        "id": session['user_id'],
        "nome": session['username'],
        "cargo": session['role']
    })
    