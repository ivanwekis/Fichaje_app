from datetime import datetime
from pydantic import BaseModel
from bson import ObjectId

class Start(BaseModel):
    start: str = None
    string_id: str = None
    date: str = None
    finish: str = "-"
    modified: bool = False
    nightShift: bool

