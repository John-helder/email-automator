from src.services.ia_service import generete_ia_response

def handle_ia_request(prompt: str):
    if not prompt:
        return {"error": "O prompt nao pode estar vazio"}
    
    result = generete_ia_response(prompt)
    return {"response": result}