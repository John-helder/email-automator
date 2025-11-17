from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

from src.services.auto_responder import gerar_resposta
from src.controllers.ia_controller import handle_ia_request
from src.controllers.email_controller import handle_email_analysis
from src.auth.routes.auth_router import get_current_user
from .nlp_utils import preprocess_text, classificar_email, gerar_resposta as nlp_gerar_resposta

router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str

@router.post("/ask")
def ask_ia(payload: PromptRequest):
    result = handle_ia_request(payload.prompt)
    return {"response": result}

class EmailRequest(BaseModel):
    texto: str

@router.post("/analyze-email")
async def analyze_email(request: EmailRequest):
    try:
        result = handle_email_analysis(request.texto)
        response = {
            "importante": result.get("importante", False),
            "exige_resposta": result.get("exige_resposta", False),
            "resumo_curto": result.get("resumo_curto", ""),
            "prioridade": result.get("prioridade", "baixa")
        }
        return {"resultado": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/auto-reply")
async def auto_reply(request: EmailRequest):
    try:
        resposta = gerar_resposta(request.texto)
        return {"resposta": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.post("/ia/analisar-nlp")
def analisar_email_nlp(request: EmailRequest, current_user: dict = Depends(get_current_user)):
    texto = request.texto
    if not texto:
        raise HTTPException(status_code=400, detail="Texto não fornecido")

    categoria = classificar_email(texto)

    resposta = nlp_gerar_resposta(categoria)

    return {
        "usuario": current_user["email"],
        "categoria": categoria,
        "resposta_sugerida": resposta
    }

