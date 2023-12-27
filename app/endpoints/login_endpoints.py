from fastapi import HTTPException, APIRouter
from app.models.login_user import LoginUser
from app.db_connection import MongoDBConnection
from app import DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION
from app.security.security import create_access_token
from app.security import passwords


router = APIRouter()
mongo_users = MongoDBConnection(DB_USER, URI_PASSWORD, DB_NAME, USERS_COLLECTION)


@router.post("/login")
def login(user: LoginUser):
    query = {
        "$or": [{"username": user.username}, {"email": user.email}],
    }
    user_data = mongo_users.find_user(query)
    if user_data is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not passwords.verify_password(user.password, user_data["password"].decode("utf-8")):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(user.username)
    print(user_data)
    return {"access_token": access_token, "token_type": "bearer", "name": user_data["name"]}
    


@router.post("/reset-password")
def reset_password(user: LoginUser):
    # Aquí iría la lógica para enviar un correo de recuperación
    # de contraseña al usuario
    return {"message": "Password reset email sent"}
