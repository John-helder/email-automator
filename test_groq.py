import os
from groq import Groq
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
print("API carregada?", API_KEY is not None)

client = Groq(api_key=API_KEY)

def analisar_email(email: str):
    prompt = f"""
    Você é um analisador de emails. Leia o texto abaixo e diga:
    - Se o email é importante ou não
    - Se exige resposta
    - Um resumo curto
    - A prioridade (alta, média, baixa)

    Email:
    {email}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # modelo grátis
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    # 👇 Correção aqui!
    return response.choices[0].message.content


if __name__ == "__main__":
    email = """
    Olá John, tudo bem?

    Você poderia me enviar o relatório atualizado até o final do dia?
    Obrigado!
    """

    resultado = analisar_email(email)
    print("\nResultado da análise:\n")
    print(resultado)
