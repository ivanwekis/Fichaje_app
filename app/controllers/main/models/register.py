from pydantic import BaseModel


class Register(BaseModel):

    string_id: str = None
    date : str = None
    start: str = None
    finish: str = None
    modified: bool = False
    nightShift: bool = False


    