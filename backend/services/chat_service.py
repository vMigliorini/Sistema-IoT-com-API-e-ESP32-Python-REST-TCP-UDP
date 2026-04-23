from extensions import db
from sqlalchemy import select, func, update, delete
from sqlalchemy.exc import SQLAlchemyError
from models import Usuario, CargoEnum, EspDevice, ChatRoom, RoomDevice, ChatMessage, LeituraESP, UsuarioChat, StatusConexaoEnum

def listar_nome_users(room_id):

    try:
        resultados = (
            db.session.query(Usuario.nome)
            .join(UsuarioChat, Usuario.id == UsuarioChat.id_usuario)
            .filter(
                UsuarioChat.status == StatusConexaoEnum.conectado,
                UsuarioChat.room_id == room_id
            )
            .all()
        )
    except SQLAlchemyError as erro:
        return None, erro

    lista_de_nomes = [usuario[0] for usuario in resultados]

    return lista_de_nomes, None


def listar_salas():

    try:
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
    except SQLAlchemyError as erro:
        return None, erro
    return contagens, None


def limpar_salas_vazias():
    try:
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

        if not rooms_vazias:
            return None

        db.session.execute(delete(UsuarioChat).where(UsuarioChat.room_id.in_(rooms_vazias)))
        db.session.execute(delete(ChatRoom).where(ChatRoom.id.in_(rooms_vazias)))
        db.session.commit()

    except SQLAlchemyError as erro:
        db.session.rollback()
        return erro
    
    return None


def criar_sala(nome_sala, user_id):
    

    if not nome_sala:
        return None, "Campo nome da sala obrigatório"

    if db.session.execute(select(ChatRoom).where(ChatRoom.nome == nome_sala)).scalar():
        return None, "Esse nome de sala já existe"

    try:
        novo = ChatRoom(nome=nome_sala)
        db.session.add(novo)
        db.session.commit()
    
        membro = UsuarioChat(id_usuario=user_id, room_id=novo.id)
        db.session.add(membro)
        db.session.commit()

    except SQLAlchemyError as erro:
        db.session.rollback()
        return None, erro

    return novo, None
