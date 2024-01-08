from re import search
from app.models.modify_user import ModifyUser
from fastapi import APIRouter, Depends
from app.models.user import User
from app.controllers.main.models.register import Register
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
import logging
from app.security.security import oauth2_scheme, get_current_user, get_user
from app.controllers.main.handlers import userinfo, registers


logger = logging.getLogger(__name__)
router = APIRouter()

mongo_users = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION)
mongo_collections = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME)
register_list = ["id", "date", "start", "finish", "modified", "nightShift", "reason"]


@router.post("/v2/getregisters/{page}")
async def get_registers(page: int, user: User, token: str = Depends(oauth2_scheme)):
    get_current_user(token, username=user.username)
    return registers.get_registers(page, mongo_users, mongo_collections, user)


@router.put("/v2/modifyRegister")
async def modify_register(register: Register, token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    return registers.modify_register(mongo_users, mongo_collections, user, register)


@router.get("/v2/searchregisters/{searchText}")
async def search_register(searchText: str, token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    return registers.search_register(searchText, mongo_collections, user)


@router.get("/v2/getregisterslength")
async def get_registers_lenght(token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    return registers.get_registers_lenght(mongo_users, mongo_collections, user)


@router.get("/v2/getuserinfo")
async def get_user_info(token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    return userinfo.get_user_info(mongo_users, user)


@router.put("/v2/modifyuserinfo")
async def modify_user(modifyUser: ModifyUser, token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    return userinfo.modify_user(mongo_users, user, modifyUser)
