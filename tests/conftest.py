import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient
from app.endpoints import login_endpoints,admin_endpoints, fichaje_endpoints

@pytest.fixture(scope="module")
def app():
    # Create a FastAPI app instance
    app = FastAPI()
    app.include_router(login_endpoints.router)
    app.include_router(admin_endpoints.router)
    app.include_router(fichaje_endpoints.router)


@pytest.fixture(scope="module")
def client(app):
    # Create a test client using the app instance
    client = TestClient(app)
    return client
