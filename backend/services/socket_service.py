from extensions import db
from sqlalchemy import select, func, update, delete
from sqlalchemy.exc import SQLAlchemyError
from models import Usuario, CargoEnum, EspDevice, ChatRoom, RoomDevice, ChatMessage, LeituraESP, UsuarioChat, StatusConexaoEnum

def entrar_sala(room_id, user_id):
    if not room_id or not user_id:
        return None, "Erro! id da sala ou do user é null"

    try:
        sala = db.session.get(ChatRoom, room_id)
    
        if not sala:
            return None, "Sala não encontrada"

        stmt = select(UsuarioChat).where(UsuarioChat.id_usuario == user_id, UsuarioChat.room_id == room_id)
        membro = db.session.execute(stmt).scalar()
    
        if membro:
            membro.status = StatusConexaoEnum.conectado
        else:
            membro = UsuarioChat(id_usuario=user_id, room_id=room_id)
            db.session.add(membro)
        db.session.commit()
        return True, None

    except SQLAlchemyError as erro:
        db.session.rollback()
        return None, erro

def atualizar_desconexao(user_id):
    if not user_id:
        return None, "Erro! usuário sem id definido"
    
    try:
        stmt = (
                update(UsuarioChat)
                .where(UsuarioChat.id_usuario == user_id)
                .values(status=StatusConexaoEnum.desconectado)
            )
        db.session.execute(stmt)
        db.session.commit()
    except SQLAlchemyError as erro:
        db.session.rollback()
        return None, erro
    return True, None