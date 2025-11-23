from unittest.mock import patch
from jose import jwt

SECRET = "dev-secret"
ALGO = "HS256"

def test_ask_ia(client):
    with patch("src.controllers.ia_controller.handle_ia_request") as mock_ia:
        mock_ia.return_value = "Resposta gerada"

        response = client.post("/ask", json={"prompt": "Olá IA"})

        assert response.status_code == 200
        assert response.json()["response"] == "Resposta gerada"
        mock_ia.assert_called_once()

def test_analyze_email_success(client):
    fake_result = {
        "importante": True,
        "exige_resposta": True,
        "resumo_curto": "Pergunta sobre compra",
        "prioridade": "alta"
    }

    with patch("src.controllers.email_controller.handle_email_analysis") as mock_analysis:
        mock_analysis.return_value = fake_result

        response = client.post("/analyze-email", json={"texto": "Quero saber o status da compra"})

        assert response.status_code == 200
        data = response.json()["resultado"]

        assert data["importante"] is True
        assert data["prioridade"] == "alta"

def test_analyze_email_internal_error(client):
    with patch("src.controllers.email_controller.handle_email_analysis") as mock_analysis:
        mock_analysis.side_effect = Exception("Falha interna")

        response = client.post("/analyze-email", json={"texto": "teste"})

        assert response.status_code == 500
        assert "Erro interno" in response.json()["detail"]


def test_auto_reply_success(client):
    with patch("src.services.auto_responder.gerar_resposta") as mock_reply:
        mock_reply.return_value = "Aqui está sua resposta automática."

        response = client.post("/auto-reply", json={"texto": "preciso da nota fiscal"})

        assert response.status_code == 200
        assert response.json()["resposta"] == "Aqui está sua resposta automática."
        mock_reply.assert_called_once()


def test_auto_reply_error(client):
    with patch("src.services.auto_responder.gerar_resposta") as mock_reply:
        mock_reply.side_effect = Exception("Falha de IA")

        response = client.post("/auto-reply", json={"texto": "teste"})

        assert response.status_code == 500
        assert "Erro interno" in response.json()["detail"]

def test_analisar_nlp_success(client):
    
    with patch("src.routes.nlp_utils.classificar_email") as mock_classificar:
        mock_classificar.return_value = "financeiro"

        with patch("src.routes.nlp_utils.gerar_resposta") as mock_gerar:
            mock_gerar.return_value = "Resposta sugerida financeiramente."

            
            token = jwt.encode({"sub": "user@example.com"}, SECRET, algorithm=ALGO)

            response = client.post(
                "/ia/analisar-nlp",
                json={"texto": "Quero atualizar meu endereço."},
                headers={"Authorization": f"Bearer {token}"}
            )

            assert response.status_code == 200
            data = response.json()

            assert data["usuario"] == "user@example.com"
            assert data["categoria"] == "financeiro"
            assert data["resposta_sugerida"] == "Resposta sugerida financeiramente."


def test_analisar_nlp_sem_texto(client):
    token = jwt.encode({"sub": "teste@teste.com"}, SECRET, algorithm=ALGO)

    response = client.post(
        "/ia/analisar-nlp",
        json={"texto": ""},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Texto não fornecido"


def test_analisar_nlp_sem_token(client):
    response = client.post(
        "/ia/analisar-nlp",
        json={"texto": "qualquer coisa"}
    )

    assert response.status_code == 401



