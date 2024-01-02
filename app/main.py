from app.controllers.admin import admin_endpoints
from app.controllers.login import login_endpoints
from app.controllers.main import dbquerys_endpoints
from app.controllers.main import fichaje_endpoints

from app import app

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
