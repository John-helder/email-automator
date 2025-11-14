from src.config.groq_cliente import get_groq_client

def generete_ia_response(prompt: str):
    client = get_groq_client()

    response = client.chat.completions.create(
        model = "llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    return response.choices[0].message["content"]