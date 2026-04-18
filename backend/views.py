from extensions import bcrypt, db
from models import Usuario, CargoEnum
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from sqlalchemy import select


views_bp = Blueprint('views', __name__)

#rotas
@views_bp.route("/chat_rooms")
def chat_rooms():
    if 'user_id' not in session:
        return redirect(url_for('views.login'))
    return render_template("chat_rooms.html")

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