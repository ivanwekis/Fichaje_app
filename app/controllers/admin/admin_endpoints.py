from fastapi import HTTPException, APIRouter
from app.models.user import User
from .models.create_user import CreateUser
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
from app.security import passwords
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

mongo_users = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION)


@router.post("/v1/create_user")
def create_user(user: CreateUser):
    logger.info(f"user: {user.username}")
    date = datetime.now()
    if mongo_users.find_user({"$or": [{"username": user.username}, {"email": user.email}]}):
        raise HTTPException(status_code=400, detail="El nombre de usuario/email ya existe en la BD")
    user.password = passwords.hash_password(user.password)
    user = user.dict()
    user.update({"date": date.strftime("%d/%m/%Y"), "time": date.strftime("%H:%M:%S")})
    mongo_users.insert_user(user)
    return {"mensaje": f"{user['username']} ha sido creado correctamente"}


@router.get("/v1/get_user")
def get_user(user: User):
    logger.info(f"user: {user.username}")
    user = mongo_users.find_user({"user": user.username})
    if user:
        return user
    raise HTTPException(status_code=400, detail="El user no existe en la BD")


@router.delete("/v1/delete_user")
def delete_user(user: User):
    logger.info(f"user: {user.username}")
    result = mongo_users.delete_user({"user": user.username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=400, detail="El user no existe en la BD")

    return {"mensaje": f"{user.username} ha sido eliminado correctamente"}


@router.put("/v1/update_user")
def update_user(user: CreateUser):
    logger.info(f"user: {user.username}")
    user = mongo_users.find_user({"user": user.username})
    if not user:
        raise HTTPException(status_code=400, detail="El user no existe en la BD")
    user = user.dict()
    mongo_users.update_user({"user": user.user}, user)
    return {"mensaje": f"{user['username']} ha sido actualizado correctamente"}
