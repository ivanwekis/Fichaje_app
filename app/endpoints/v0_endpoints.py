from fastapi import HTTPException, APIRouter
from app.classes.usuario import Usuario
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, COLLECTION_NAME
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

mongo = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, COLLECTION_NAME)


@router.post("/v0/fichar")
async def fichar(usuario: Usuario):
    logger.info(f"Usuario: {usuario.user}")
    # Verifica si el usuario ya existe en la base de datos
    if mongo.find_user({"user": usuario.user}):
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    else:
        mongo.insert_user(usuario.dict())
        return {"mensaje": f"{usuario.user} ha fichado correctamente"}


@router.post("/v0/desfichar")
async def desfichar(usuario: Usuario):
    logger.debug(f"Usuario: {usuario.user}")
    # Verifica si el usuario ya existe en la base de datos
    response = mongo.delete_user({"user": usuario.user})
    if response.deleted_count == 0:
        raise HTTPException(status_code=404, detail="El usuario no existe")
    return {"mensaje": f"{usuario.user} ha desfichado correctamente"}
