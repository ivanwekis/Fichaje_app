from fastapi import HTTPException
from app.security import passwords


def get_user_info(mongo_users, user):
    user_data = mongo_users.find_user({"username": user.username})
    if user_data:
        return {
            "name": user_data["name"],
            "username": user_data["username"],
            "surname": user_data["surname"],
            "email": user_data["email"],
            "company": user_data["company"],
        }

    else:
        raise HTTPException(status_code=403, detail="Incorrect username.")


def modify_user(mongo_users, user, modifyUser):
    new_password = passwords.hash_password(modifyUser.password)
    count = mongo_users.update_user(
        {"username": user.username},
        {
            "username": modifyUser.username,
            "email": modifyUser.email,
            "password": new_password,
            "name": modifyUser.name,
            "surname": modifyUser.surname,
            "company": modifyUser.company,
        },
    )
    if count:
        return {"message": "The user has been modified successfully."}
    else:
        raise HTTPException(
            status_code=404, detail="There was an error modifying the user."
        )
