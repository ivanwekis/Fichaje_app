from fastapi import APIRouter
from app.models.user import User
from .models.create_user import CreateUser
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
import logging
from app.controllers.admin.handlers import users

logger = logging.getLogger(__name__)
router = APIRouter()

mongo_users = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION)


@router.get("/v1/get_user")
def get_user(user: User):
    return users.get_users(mongo_users, user)


@router.post("/v1/create_user")
def create_user(user: CreateUser):
    return users.create_user(mongo_users, user)


@router.delete("/v1/delete_user")
def delete_user(user: User):
    return users.delete_user(mongo_users, user)


@router.put("/v1/update_user")
def update_user(user: CreateUser):
    return users.update_user(mongo_users, user)
