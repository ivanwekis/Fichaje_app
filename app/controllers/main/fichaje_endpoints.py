from fastapi import HTTPException, APIRouter, Depends
from app.controllers.main.models.register import Input
from app.controllers.main.models.register import Register
from app.controllers.main.models.output import Output
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
import logging
from datetime import datetime
from app.security.security import oauth2_scheme, get_user


logger = logging.getLogger(__name__)
router = APIRouter()

mongo_users = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION)
mongo_collections = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME)


@router.post("/v0/fichar")
async def fichar(register: Register, token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    if mongo_users.find_user({"username": user.username}):
        mongo_collections._set_collection(user.username)
        date = datetime.now()
        ## wether the user has already started the day and wants to start again.
        if mongo_collections.find_user({"date": date.strftime("%d/%m/%Y")}):
            filter = {"date": date.strftime("%d/%m/%Y")}
            input = Input()
            input.input = date.strftime("%H:%M")
            output = Output()
            output.output = "-"
            output.reason = "-"
            mongo_collections.more_than_one(filter, {"$push": {"inputs": {"$each": [input.dict()]}, "outputs": {"$each": [output.dict()]}}})
        ## wether the user has not started the day yet.
        else:
            register.string_id = date.strftime("%d/%m/%Y%H:%M:%S")
            register.date = date.strftime("%d/%m/%Y")
            input = Input()
            input.input = date.strftime("%H:%M")
            register.inputs.append(input)
            output = Output()
            output.output = "-"
            output.reason = "-"
            register.outputs.append(output)
            register_dict = register.dict()
            register_dict.update({"_id": date})
            mongo_collections.insert_user(register_dict)
        return {"mensaje": f"{user.username} ha fichado correctamente"}
    else:
        raise HTTPException(status_code=400, detail="El user no existe en la BD")


@router.post("/v0/desfichar")
async def desfichar(output: Output, token: str = Depends(oauth2_scheme)):
    user = get_user(token)
    # Verifica si el user ya existe en la base de datos
    if mongo_users.find_user({"username": user.username}):
        mongo_collections._set_collection(user.username)
        date = datetime.now()
        if mongo_collections.find_user({"date": date.strftime("%d/%m/%Y")}):
            filter = {"date": date.strftime("%d/%m/%Y")}
            outputs = mongo_collections.find_user(filter)["outputs"]
            if outputs:
                outputs[-1]["output"] = date.strftime("%H:%M")
                outputs[-1]["reason"] = output.reason
                mongo_collections.update_one_register(filter, {"outputs": outputs})
                print(outputs[-1])
                return {"mensaje": f"{user.username} ha desfichado correctamente"}
            else:
                raise HTTPException(status_code=400, detail="No ha fichado aun hoy")
            
        else:
            raise HTTPException(status_code=400, detail="No ha fichado aun hoy")
    else:
        raise HTTPException(status_code=404, detail="El user no existe en la BD")
