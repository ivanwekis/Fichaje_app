from app import app
from app.endpoints import admin_endpoints, login_endpoints, fichaje_endpoints

app.include_router(login_endpoints.router)
app.include_router(admin_endpoints.router)
app.include_router(fichaje_endpoints.router)
