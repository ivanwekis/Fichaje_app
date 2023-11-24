from app import app
from app.endpoints import v0_endpoints
from app.endpoints import v1_endpoints


app.include_router(v0_endpoints.router)
app.include_router(v1_endpoints.router)
