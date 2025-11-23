def test_email_analyzer(client, user_payload):
    client.post("/register", json=user_payload)
    token = client.post("/login", json=user_payload).json()["access_token"]

    payload = {"email_text": "Olá, gostaria de saber o status do projeto."}

    response = client.post(
        "/email_analyzer",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "analysis" in response.json()


def test_auto_reply(client, user_payload):
    client.post("/register", json=user_payload)
    token = client.post("/login", json=user_payload).json()["access_token"]

    payload = {"email_text": "Quando meu boleto é gerado?"}

    response = client.post(
        "/auto_replay",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "reply" in response.json()


def test_analyser_nlp(client, user_payload):
    client.post("/register", json=user_payload)
    token = client.post("/login", json=user_payload).json()["access_token"]

    payload = {"text": "Preciso atualizar meu endereço."}

    response = client.post(
        "/analiser_nlp",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "result" in response.json()
