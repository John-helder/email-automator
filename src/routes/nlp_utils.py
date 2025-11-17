import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")
stop_words = set(stopwords.words("portuguese"))

def preprocess_text(texto: str):
    texto = re.sub(r"[^a-zA-ZçÇáéíóúãõâêîôû\s]", "", texto)
    texto = texto.lower()
    palavras = [w for w in texto.split() if w not in stop_words]
    return " ".join(palavras)

def classificar_email(texto: str):
    palavras_chave_produtivo = ["solicito", "preciso", "erro", "atualização", "reunião", "pendente"]
    texto_proc = preprocess_text(texto)
    
    if any(p in texto_proc for p in palavras_chave_produtivo):
        return "Produtivo"
    else:
        return "Improdutivo"

def gerar_resposta(categoria: str):
    if categoria == "Produtivo":
        return "Obrigado pelo contato! Vamos analisar sua solicitação e responder o mais breve possível."
    else:
        return "Agradecemos sua mensagem!"
