
from src.services.email_analyzer import analisar_email

def handle_email_analysis(texto: str):
    """
    Função de controller para análise de emails.
    Recebe o texto do email e retorna o dicionário com a análise.
    """
    result = analisar_email(texto)
    
    # Garante que o resultado sempre tenha todas as chaves esperadas
    response = {
        "importante": result.get("importante", False),
        "exige_resposta": result.get("exige_resposta", False),
        "resumo_curto": result.get("resumo_curto", ""),
        "prioridade": result.get("prioridade", "baixa")
    }
    
    return response
