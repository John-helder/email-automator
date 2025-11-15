from src.services.email_analyzer import analisar_email

def gerar_resposta(email_texto: str) -> str:

    analise = analisar_email(email_texto)

    # Garantir que a análise tenha todos os campos
    importante = analise.get("importante", False)
    exige_resposta = analise.get("exige_resposta", False)
    prioridade = analise.get("prioridade", "baixa")

    # Definir a resposta automática
    if importante and exige_resposta:
        resposta = (
            f"Obrigado pelo seu email. Recebi sua mensagem e estou trabalhando para atender "
            f"sua solicitação com prioridade {prioridade}."
        )
    elif importante and not exige_resposta:
        resposta = "Obrigado pelo email. Tomarei ciência das informações."
    elif not importante and exige_resposta:
        resposta = "Recebi sua mensagem e responderei assim que possível."
    else:
        resposta = "Mensagem recebida, obrigado."

    return resposta

