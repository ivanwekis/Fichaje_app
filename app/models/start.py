import datetime
from pydantic import BaseModel


class Start(BaseModel):
    start: str = None
    _id: datetime.datetime = None
    string_id: str = None
    date: str = None
    finish: str = None
    nightShift: bool

