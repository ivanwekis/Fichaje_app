from pydantic import BaseModel


class Register(BaseModel):
    id: str
    date : str 
    start: str
    finish: str