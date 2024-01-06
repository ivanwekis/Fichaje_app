from app.security.security import create_access_token
from app.security import passwords
from fastapi import HTTPException


def login_user(mongo_users, user):
    query = {
        "$or": [{"username": user.username}, {"email": user.email}],
    }
    user_data = mongo_users.find_user(query)
    if user_data is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not passwords.verify_password(
        user.password, user_data["password"].decode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(user.username)
    admin_access = user_data.get("admin_access", False)
 
    return {
        "access_token": access_token,
        "admin_access": admin_access,
        "token_type": "bearer",
        "name": user_data["name"],
    }


def reset_password():
    return {"message": "Password reset email sent"}
