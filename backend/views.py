from extensions import bcrypt, db
from models import Usuario
from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import select


views_bp = Blueprint('views', __name__)

#rotas
@views_bp.route("/homepage")
def homepage():
    return render_template("homepage.html")

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
        return jsonify({"ok": True}), 201
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

    stmt = select(Usuario).where(Usuario.email == email)
    usuario_existente = db.session.execute(stmt).scalar()
    if usuario_existente:
        return jsonify({"ok": False, "erro": "E-mail já cadastrado"}), 400

    hash_senha = bcrypt.generate_password_hash(senha).decode("utf-8")
    novo = Usuario(nome=nome, email=email, senha_hash=hash_senha)
    db.session.add(novo)
    db.session.commit()
    return jsonify({"ok": True}), 201
