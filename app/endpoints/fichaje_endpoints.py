from fastapi import HTTPException, APIRouter, Depends
from app.models.user import User
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
import logging
from datetime import datetime
from app.security.security import oauth2_scheme, get_current_user


logger = logging.getLogger(__name__)
router = APIRouter()

mongo_users = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION)
mongo_collections = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME)


@router.post("/v0/fichar")
async def fichar(user: User, token: str = Depends(oauth2_scheme)):
    user_by_token = get_current_user(token, username=user.username)
    if mongo_users.find_user({"username": user.username}):
        print(f"User: {user_by_token}")
        mongo_collections._set_collection(user.username)
        date = datetime.now()
        if mongo_collections.find_user({"date": date.strftime("%d/%m/%Y")}):
            raise HTTPException(status_code=400, detail="El user ya ha fichado hoy")
        document = {
            "_id": date,
            "date": date.strftime("%d/%m/%Y"),
            "start": date.strftime("%H:%M"),
            "finish": "-"
        }
        mongo_collections.insert_user(document)
        return {"mensaje": f"{user.username} ha fichado correctamente"}
    else:
        raise HTTPException(status_code=400, detail="El user no existe en la BD")


@router.post("/v0/desfichar")
async def desfichar(user: User, token: str = Depends(oauth2_scheme)):
    get_current_user(token, username=user.username)
    logger.debug(f"user: {user.username}")
    # Verifica si el user ya existe en la base de datos
    if mongo_users.find_user({"username": user.username}):
        mongo_collections._set_collection(user.username)
        date = datetime.now()
        if mongo_collections.find_user(
            {"date": date.strftime("%d/%m/%Y")}
        ):
            filter = {"date": date.strftime("%d/%m/%Y")}    
            document = {
                "finish": date.strftime("%H:%M")
            }
            mongo_collections.update_one_register(filter, document)
            return {"mensaje": f"{user.username} ha desfichado correctamente"}
        else:
            raise HTTPException(status_code=400, detail="No ha fichado aun hoy")
