from fastapi import HTTPException, APIRouter
from app.classes.user import User
from app.classes.create_user import CreateUser
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

mongo_users = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION)


@router.post("/v1/create_user")
def create_user(user: CreateUser):
    logger.info(f"user: {user.user}")
    date = datetime.now()
    if mongo_users.find_user({"user": user.user}):
        raise HTTPException(status_code=400, detail="El user ya existe en la BD")
    user = user.dict()
    user.update({"date": date.strftime("%d/%m/%Y"), "time": date.strftime("%H:%M:%S")})
    mongo_users.insert_user(user)
    return {"mensaje": f"{user['user']} ha sido creado correctamente"}


@router.get("/v1/get_user")
def get_user(user: User):
    logger.info(f"user: {user.user}")
    user = mongo_users.find_user({"user": user.user})
    if user:
        return user
    raise HTTPException(status_code=400, detail="El user no existe en la BD")


@router.delete("/v1/delete_user")
def delete_user(user: User):
    logger.info(f"user: {user.user}")
    result = mongo_users.delete_user({"user": user.user})
    if result.deleted_count == 0:
        raise HTTPException(status_code=400, detail="El user no existe en la BD")
    
    return {"mensaje": f"{user.user} ha sido eliminado correctamente"}


@router.put("/v1/update_user")
def update_user(user: CreateUser):
    logger.info(f"user: {user.user}")
    user = mongo_users.find_user({"user": user.user})
    if not user:
        raise HTTPException(status_code=400, detail="El user no existe en la BD")
    user = user.dict()
    mongo_users.update_user({"user": user.user}, user)
    return {"mensaje": f"{user['user']} ha sido actualizado correctamente"}
