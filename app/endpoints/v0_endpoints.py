from fastapi import HTTPException, APIRouter
from app.classes.user import User
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

mongo_users = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION)
mongo_collections = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME)


@router.post("/v0/fichar")
async def fichar(user: User):
    logger.info(f"user: {user.user}")
    mongo_users.insert_user({"user": user.user})
    if mongo_users.find_user({"user": user.user}):
        mongo_collections._set_collection(user.user)
        date = datetime.now()
        if mongo_collections.find_user({"date": date.strftime("%d/%m/%Y")}):
            raise HTTPException(status_code=400, detail="El user ya ha fichado hoy")
        document = {
            "action": "fichar",
            "date": date.strftime("%d/%m/%Y"),
            "time": date.strftime("%H:%M:%S"),
        }
        mongo_collections.insert_user(document)
        return {"mensaje": f"{user.user} ha fichado correctamente"}
    else:
        raise HTTPException(status_code=400, detail="El user no existe en la BD")


@router.post("/v0/desfichar")
async def desfichar(user: User):
    logger.debug(f"user: {user.user}")
    # Verifica si el user ya existe en la base de datos
    if mongo_users.find_user({"user": user.user}):
        mongo_collections._set_collection(user.user)
        date = datetime.now()
        if mongo_collections.find_user(
            {"date": date.strftime("%d/%m/%Y"), "action": "fichar"}
        ):
            if mongo_collections.find_user(
                {"date": date.strftime("%d/%m/%Y"), "action": "desfichar"}
            ):
                raise HTTPException(
                    status_code=400, detail="El user ya ha desfichado hoy"
                )
            document = {
                "action": "desfichar",
                "date": date.strftime("%d/%m/%Y"),
                "time": date.strftime("%H:%M:%S"),
            }
            mongo_collections.insert_user(document)
            return {"mensaje": f"{user.user} ha desfichado correctamente"}
        else:
            raise HTTPException(
                status_code=400, detail="El user no ha fichado aun hoy"
            )
