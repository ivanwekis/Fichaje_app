import pytest
from fastapi import HTTPException
from starlette.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_login_successful(client):
    response = client.post(
        "/login",
        json={"username": "Martiita99", "password": "jcsuisiosdlks"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_incorrect_credentials(client):
    response = client.post(
        "/login",
        json={"username": "testuser", "password": "incorrectpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_reset_password(client):
    response = client.post("/reset-password", json={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset email sent"

