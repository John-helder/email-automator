import pytest
from fastapi.testclient import TestClient
from main import app  
from unittest.mock import MagicMock
from src.database import get_db


@pytest.fixture(autouse=True)
def override_db():

    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db
    yield
    app.dependency_overrides.pop(get_db)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def user_payload():
    return {"email": "test@example.com", "senha": "123456"}
