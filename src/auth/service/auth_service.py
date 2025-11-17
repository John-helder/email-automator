from sqlalchemy.orm import Session
from src.auth.models.user_model import User
from src.auth.security.hash import gerar_hash, verificar_senha
from src.auth.security.jwt_handler import criar_access_token

def create_user(db: Session, email: str, senha: str):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return None

    novo = User(email=email, senha_hash=gerar_hash(senha))
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def authenticate_user(db: Session, email: str, senha: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verificar_senha(senha, user.senha_hash):
        return False

    token = criar_access_token(user.email)
    return token
