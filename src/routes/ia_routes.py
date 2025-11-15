from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.services.auto_responder import gerar_resposta
from src.controllers.ia_controller import handle_ia_request
from src.controllers.email_controller import handle_email_analysis

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
