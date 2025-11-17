from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    senha: str

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str
