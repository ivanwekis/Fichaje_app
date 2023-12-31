from pydantic import BaseModel


class ModifyUser(BaseModel):
    username: str = None
    email: str = None
    password: str = None
    name: str = None
    surname: str = None
    company: str = None   
