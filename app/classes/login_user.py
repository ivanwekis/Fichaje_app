from pydantic import BaseModel


class LoginUser(BaseModel):
    username: str = None
    email: str = None
    password: str
