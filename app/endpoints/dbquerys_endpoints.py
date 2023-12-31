import re
from app.models.modify_user import ModifyUser
from fastapi import HTTPException, APIRouter, Depends
from app.models.user import User
from app.models.register import Register
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
import logging
from datetime import datetime
from app.security.security import oauth2_scheme, get_current_user, get_user
from app.security import passwords


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
    

@router.get("/v2/getuserinfo")
async def get_register(token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    user_data = mongo_users.find_user({"username": user.username})
    if user_data:
        return {"name": user_data["name"], "username":user_data["username"] , "surname": user_data["surname"], 
                "email": user_data["email"], "company": user_data["company"]}
        
    else:
        raise HTTPException(status_code=403, detail="Incorrect username.")
    

@router.put("/v2/modifyuserinfo")
async def modify_user(modifyUser: ModifyUser, token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    new_password = passwords.hash_password(modifyUser.password)
    count = mongo_users.update_user({"username": user.username}, {"username": modifyUser.username,
                                    "email": modifyUser.email,"password": new_password, "name": modifyUser.name,
                                    "surname": modifyUser.surname, "company": modifyUser.company})
    if count:
        return {"message":"The user has been modified successfully."}
    else:
        raise HTTPException(status_code=404, detail="There was an error modifying the user.")
         