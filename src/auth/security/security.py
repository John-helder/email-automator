from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import os

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

def gerar_hash(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha, senha_hash):
    return pwd_context.verify(senha, senha_hash)

def criar_token(data: dict, expira_minutos: int = 120):
    dados = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=expira_minutos)
    dados.update({"exp": expira})
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)
