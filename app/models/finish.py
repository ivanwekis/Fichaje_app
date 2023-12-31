from pydantic import BaseModel


class Finish(BaseModel):
    reason: str = None
    finish: str = None
