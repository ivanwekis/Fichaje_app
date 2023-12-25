import re
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


@router.post("/v2/getregisters")
async def get_registers(user: User, token: str = Depends(oauth2_scheme)):
    get_current_user(token, username=user.username)
    if mongo_users.find_user({"username": user.username}):
        mongo_collections._set_collection(user.username)
        registers = mongo_collections.find_all_sort_by_date({})
        registers_list = []
        for register in registers:
            if "finish" not in register:
                register["finish"] = "-"
            register = {"date":register["date"], "start":register["start"], "finish":register["finish"]}
            registers_list.append(register)
        
        return {"registers": registers_list}
    