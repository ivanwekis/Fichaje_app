from fastapi import APIRouter
from .models.login_user import LoginUser
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
from app.controllers.login.handlers import login

router = APIRouter()
mongo_users = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION)


@router.post("/login")
def login_user(user: LoginUser):
    return login.login_user(mongo_users, user)


@router.post("/reset-password")
def reset_password(user: LoginUser):
    return {"message": "Password reset email sent"}
