# src/services/email_analyzer.py

import json
import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analisar_email(texto: str):

    prompt = f"""
    Analise o email abaixo e responda SOMENTE com um JSON válido, no formato:

    {{
        "importante": true/false,
        "exige_resposta": true/false,
        "resumo_curto": "...",
        "prioridade": "alta/média/baixa"
    }}

    Email:
    {texto}
    """

   
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  
        messages=[{"role": "user", "content": prompt}]
    )

    
    raw = response.choices[0].message.content

    clean = raw.replace("```json", "").replace("```", "").strip()

    
    try:
        data = json.loads(clean)
    except Exception:
        return {"erro": "Resposta inválida do modelo", "conteudo": clean}

    return {
        "importante": data.get("importante", False),
        "exige_resposta": data.get("exige_resposta", False),
        "resumo_curto": data.get("resumo_curto", ""),
        "prioridade": data.get("prioridade", "baixa")
    }
