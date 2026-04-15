from main import app
from main import app, bcrypt, db
from models import Usuario
from flask import render_template, request, jsonify
from flask_cors import CORS

CORS(app)

#rotas
@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "GET":
        return render_template("cadastro.html")
    
    dados_cadastro = request.json
    nome = dados_cadastro["nome"]
    email = dados_cadastro["email"]
    senha = dados_cadastro["senha"]

    hash_senha = bcrypt.generate_password_hash(senha).decode("utf-8")
    novo = Usuario(nome=nome, email=email, senha_hash=hash_senha)
    db.session.add(novo)
    db.session.commit()
    return jsonify({"ok": True}), 201