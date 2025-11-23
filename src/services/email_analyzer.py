import json
import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

EXPECTED_SCHEMA = {
    "importante": bool,
    "exige_resposta": bool,
    "resumo_curto": str,
    "prioridade": str,
}

def validar_esquema(data: dict) -> dict:
    resltado = {}

    for campo, tipo in EXPECTED_SCHEMA.items():
        valor = data.get(campo)

        if isinstance(valor, tipo):
            resltado[campo] = valor
        else:
            if tipo == bool:
                resltado[campo] = False
            elif tipo == str:
                resltado[campo] = ""
            else:
                resltado[campo] = None
    return resltado

def analisar_email(texto: str) -> dict:
    prompt = f""" 
    Voce é um analisador de emails.
    Responda SOMENTE com um JSON valido.

    Fomato obrigatorio:
    {{
        "importante": true/false,
        "exige_resposta": true/false,
        "resumo_curto": "string",
        "prioridade": "alta/média/baixa"
    }}

    Email a ser analisado:
    {texto}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Responda sempre em JSON puro e valido."},
            {"role": "user", "content": prompt}
        ]
    )


    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", " ").strip()
    try:
        json_data = json.loads(clean)
    except json.JSONDecodeError:
        return {
            "erro": "Modelo retornou JSON invalido.",
            "conteúdo": clean
        }
    return validar_esquema(json_data)