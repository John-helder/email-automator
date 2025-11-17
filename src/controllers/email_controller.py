
from src.services.email_analyzer import analisar_email

def handle_email_analysis(texto: str):
  
    result = analisar_email(texto)
    
    
    response = {
        "importante": result.get("importante", False),
        "exige_resposta": result.get("exige_resposta", False),
        "resumo_curto": result.get("resumo_curto", ""),
        "prioridade": result.get("prioridade", "baixa")
    }
    
    return response
