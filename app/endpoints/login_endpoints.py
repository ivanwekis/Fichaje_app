from fastapi import HTTPException, APIRouter
from app.classes.login_user import LoginUser
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
from app.security import create_access_token


router = APIRouter()
mongo_users = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION)


@router.post("/login")
def login(user: LoginUser):
    query = {
        "password": user.password,
        "$or": [{"username": user.username}, {"email": user.email}],
    }
    if mongo_users.find_user(query):
        access_token = create_access_token(user.username)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@router.post("/reset-password")
def reset_password(user: LoginUser):
    # Aquí iría la lógica para enviar un correo de recuperación
    # de contraseña al usuario
    return {"message": "Password reset email sent"}
