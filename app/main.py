from app import app
from app.endpoints import v0_endpoints

app.include_router(v0_endpoints.router)
