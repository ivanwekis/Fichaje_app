from app import app
from app.endpoints import admin_endpoints, login_endpoints, fichaje_endpoints, dbquerys_endpoints
from fastapi.middleware.cors import CORSMiddleware

app.include_router(login_endpoints.router)
app.include_router(admin_endpoints.router)
app.include_router(fichaje_endpoints.router)
app.include_router(dbquerys_endpoints.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
