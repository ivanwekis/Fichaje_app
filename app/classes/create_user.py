from pydantic import BaseModel


class CreateUser(BaseModel):
    user: str
    email : str
    password : str
    name : str
    surname : str
    company : str
        