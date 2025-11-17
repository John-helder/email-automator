from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.auth.service.auth_service import create_user, authenticate_user

def handle_register(db: Session, email: str, senha: str):
    user = create_user(db, email, senha)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    return {"message": "Usuário criado com sucesso", "email": user.email}

def handle_login(db: Session, email: str, senha: str):
    token = authenticate_user(db, email, senha)
    if token is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if token is False:
        raise HTTPException(status_code=401, detail="Senha incorreta")
    return {"access_token": token, "token_type": "bearer"}
