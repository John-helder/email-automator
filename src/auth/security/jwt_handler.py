import os
from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 60

def criar_access_token(sub: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    data = {"sub": sub, "exp": expire}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
