import pytest
from fastapi.testclient import TestClient
from main import app  # reemplace esto con la ruta a su aplicación FastAPI
from app.models.user import User

client = TestClient(app)
TOKEN= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlRlc3R1c2VyIi" \
"wiZXhwIjoxODgxNzExNjY0fQ.x4KTfg9ml--yl6dDpaO0gPG-FXbA9toH8znz8pvSVXo"


@pytest.mark.asyncio
async def test_fichar():
    # Crear un usuario de prueba
    test_user = User(username="testuser")
    header = {"Authorization": "Bearer {token}"}
    response = client.post("/v0/fichar",header=header  ,json=test_user.dict())
    assert response.status_code == 200
    assert response.json() == {"meznsaje": "testuser ha fichado correctamente"}


@pytest.mark.asyncio
async def test_desfichar():
    # Crear un usuario de prueba
    test_user = User(username="testuser")
    response = client.post("/v0/desfichar", json=test_user.dict())
    assert response.status_code == 200
    assert response.json() == {"mensaje": "testuser ha desfichado correctamente"}
    