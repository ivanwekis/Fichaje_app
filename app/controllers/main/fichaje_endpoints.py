from fastapi import APIRouter, Depends
from app.controllers.main.models.register import Register
from app.controllers.main.models.output import Output
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
import logging
from app.security.security import oauth2_scheme, get_user
from app.controllers.main.handlers import fichaje


logger = logging.getLogger(__name__)
router = APIRouter()

mongo_users = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION)
mongo_collections = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME)


@router.post("/v0/fichar")
async def fichar(register: Register, token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    return fichaje.fichar(mongo_users, mongo_collections, register, user)


@router.post("/v0/desfichar")
async def desfichar(output: Output, token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    return fichaje.desfichar(mongo_users, mongo_collections, output, user)
