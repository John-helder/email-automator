from fastapi import FastAPI
from src.routes.ia_routes import router as ia_router


app = FastAPI()

app.include_router(ia_router, prefix="/api")



@app.get("/")
def root():
    return {"message": "API Groq + FastAPI funcionando!"}

