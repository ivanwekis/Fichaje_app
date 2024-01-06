from fastapi import HTTPException
from datetime import datetime
from app.security import passwords


def get_users(mongo_users, user):
    user = mongo_users.find_user({"user": user.username})
    if user:
        return user
    raise HTTPException(status_code=400, detail="El user no existe en la BD")


def create_user(mongo_users, user):
    date = datetime.now()
    if mongo_users.find_user(
        {"$or": [{"username": user.username}, {"email": user.email}]}
    ):
        raise HTTPException(
            status_code=400, detail="El nombre de usuario/email ya existe en la BD"
        )
    user.password = passwords.hash_password(user.password)
    user = user.dict()
    user.update({"date": date.strftime("%d/%m/%Y"), "time": date.strftime("%H:%M:%S")})
    mongo_users.insert_user(user)
    return {"mensaje": f"{user['username']} ha sido creado correctamente"}


def delete_user(mongo_users, user):
    result = mongo_users.delete_user({"user": user.username})
    if result.deleted_count == 0:
        raise HTTPException(status_code=400, detail="El user no existe en la BD")

    return {"mensaje": f"{user.username} ha sido eliminado correctamente"}


def update_user(mongo_users, user):
    user = mongo_users.find_user({"user": user.username})
    if not user:
        raise HTTPException(status_code=400, detail="El user no existe en la BD")
    user = user.dict()
    mongo_users.update_user({"user": user.user}, user)
    return {"mensaje": f"{user['username']} ha sido actualizado correctamente"}
