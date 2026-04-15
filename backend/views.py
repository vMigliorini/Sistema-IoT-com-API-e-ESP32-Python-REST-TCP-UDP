from main import app
from flask import render_template

#rotas
@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")