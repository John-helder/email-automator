from src.services.email_analyzer import analisar_email


def gerar_resposta(email_texto: str) -> dict:

    analise = analisar_email(email_texto)

    if "erro" in analise:
        return {
            "erro": "Falha ao analisar email",
            "detalhes": analise
        }

    importante = analise["importante"]
    exige_resposta = analise["exige_resposta"]
    prioridade = analise["prioridade"]

    if importante and exige_resposta:
        resposta = (
            f"Olá! Obrigado pelo seu email. "
            f"Estou tratando sua solicitação com prioridade {prioridade}."
        )
    elif importante and not exige_resposta:
        resposta = (
            "Olá! Obrigado pelo seu email. "
            "As informações foram recebidas e registradas."
        )
    elif not importante and exige_resposta:
        resposta = (
            "Olá! Recebi sua mensagem e retornarei assim que possível."
        )
    else:
        resposta = "Olá! Mensagem recebida, obrigado."

    return {
        "analise": analise,
        "resposta_gerada": resposta
    }
