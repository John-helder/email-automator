from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.controllers.ia_controller import handle_ia_reaquest
from src.controllers.email_controller import handle_email_analysis

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/ask")
def ask_ia(payload: PromptRequest):
    """
    Recebe um prompt genérico e retorna a resposta da IA.
    """
    result = handle_ia_reaquest(payload.prompt)
    return {"response": result}


class EmailRequest(BaseModel):
    texto: str

@router.post("/analyze-email")
async def analyze_email(request: EmailRequest):
    """
    Recebe um email e retorna a análise em JSON:
    {
        "importante": bool,
        "exige_resposta": bool,
        "resumo_curto": str,
        "prioridade": str
    }
    """
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
