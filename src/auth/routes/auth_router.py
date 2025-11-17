from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from src.database import get_db
from src.auth.schemas.auth_schemas import RegisterRequest, LoginSchema
from src.auth.controller.auth_controller import handle_register, handle_login
import os

SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["Auth"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        return {"email": user_email}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )


@router.post("/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return handle_register(db, payload.email, payload.senha)


@router.post("/login")
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    return handle_login(db, payload.email, payload.senha)


@router.get("/me")
def read_me(current_user: dict = Depends(get_current_user)):
    return current_user
