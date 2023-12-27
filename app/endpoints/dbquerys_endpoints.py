import re
from fastapi import HTTPException, APIRouter, Depends
from app.models.user import User
from app.models.register import Register
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
import logging
from datetime import datetime
from app.security.security import oauth2_scheme, get_current_user, get_user


logger = logging.getLogger(__name__)
router = APIRouter()

mongo_users = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION)
mongo_collections = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME)


@router.post("/v2/getregisters/{page}")
async def get_registers(page: int, user: User, token: str = Depends(oauth2_scheme)):
    get_current_user(token, username=user.username)
    if mongo_users.find_user({"username": user.username}):
        mongo_collections._set_collection(user.username)
        registers = mongo_collections.find_all_sort_by_date({}, page)
        registers_list = []
        for register in registers:
            if "finish" not in register:
                register["finish"] = "-"
            if "modified" not in register:
                register["modified"] = False
            register = {"id":register["string_id"], "date":register["date"], "start":register["start"], 
                        "finish":register["finish"], "modified":register["modified"]}
            registers_list.append(register)
        return {"registers": registers_list}
    

@router.put("/v2/modifyRegister")
async def modify_register(register: Register, token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    if mongo_users.find_user({"username": user.username}):
        mongo_collections._set_collection(user.username)
        
        if mongo_collections.update_one_register({"string_id": register.id}, 
        {"start": register.start, "finish": register.finish, "modified": True}):
            
            return {"message":"The register has been modified successfully."}
        else:
            raise HTTPException(status_code=404, detail="The register does not exist or the id is incorrect.")
       
    else:
        raise HTTPException(status_code=403, detail="Incorrect username.")
    