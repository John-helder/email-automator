from unittest.mock import patch


def test_register(client, user_payload):
    with patch("src.auth.router.auth_router.handle_register") as mock_register:
        mock_register.return_value = {"id": 1, "email": user_payload["email"]}

        response = client.post("/auth/register", json=user_payload)

        assert response.status_code == 200
        mock_register.assert_called_once()
        assert response.json()["email"] == user_payload["email"]


def test_login(client, user_payload):
    fake_token = "jwt-token-123"

    with patch("src.auth.router.auth_router.handle_login") as mock_login:
        mock_login.return_value = {"access_token": fake_token, "token_type": "bearer"}

        response = client.post("/auth/login", json=user_payload)

        assert response.status_code == 200
        assert response.json()["access_token"] == fake_token
        mock_login.assert_called_once()


def test_me(client):

    from jose import jwt

    SECRET = "dev-secret"
    payload = {"sub": "user@example.com"}

    token = jwt.encode(payload, SECRET, algorithm="HS256")

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"
