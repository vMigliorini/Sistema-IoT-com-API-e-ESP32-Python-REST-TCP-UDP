from extensions import db, bcrypt
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from models import Usuario, CargoEnum

def cadastrar(nome, email, senha, cargo):

    if not nome or not email or not senha or not cargo:
        return None, "Erro! Faltam campos a ser preenchidos"
    try:
        cargo_enum = CargoEnum(cargo)
    except ValueError:
        return None, "Erro! Cargo inválido"

    stmt = select(Usuario).where(Usuario.email == email)
    try:
        usuario_existente = db.session.execute(stmt).scalar()
    except SQLAlchemyError as erro:
        return None, erro
    
    if usuario_existente:
        return None, "Erro! Email já cadastrado"

    hash_senha = bcrypt.generate_password_hash(senha).decode("utf-8")
    try:
        novo = Usuario(nome=nome, email=email, cargo=cargo_enum, senha_hash=hash_senha)
        db.session.add(novo)
        db.session.commit()
    except SQLAlchemyError as erro:
        return None, erro

    return True, None

def logar(email, senha):

    if not email or not senha:
        return None, "Erro! Email e senha não foram inseridos"

    stmt = select(Usuario).where(Usuario.email == email)
    try:
        usuario = db.session.execute(stmt).scalar()
    except SQLAlchemyError as erro:
        return None, erro

    if not usuario:
        return None, "Erro! Usuário ainda não cadastrado"
    
    senha_valida = bcrypt.check_password_hash(usuario.senha_hash, senha)

    if senha_valida:
        return ({"id": usuario.id, "nome": usuario.nome, "cargo": usuario.cargo.value}), None
    else:
        return None, "Erro! Senha inválida"