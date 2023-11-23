from fastapi import HTTPException, APIRouter
from app.classes.usuario import Usuario
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, COLLECTION_NAME


router = APIRouter()

mongo = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, COLLECTION_NAME)

usuarios_db = {}


@router.post("/v0/fichar")
async def fichar(usuario: Usuario):
    # Verifica si el usuario ya existe en la base de datos

    if usuario.user in usuarios_db:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Almacena el usuario en la base de datos (en este caso, en memoria)
    usuarios_db[usuario.user] = usuario

    return {"mensaje": f"{usuario.user} ha fichado correctamente"}


@router.post("/v0/desfichar")
async def desfichar(usuario: Usuario):
    # Verifica si el usuario ya existe en la base de datos
    if usuario.user in usuarios_db:
        user = usuarios_db.pop(usuario.user)
        return {"mensaje": f"{user.user} ha desfichado correctamente"}

    raise HTTPException(status_code=400, detail="El usuario no existe")
