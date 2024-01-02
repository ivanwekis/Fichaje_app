from pydantic import BaseModel


class Output(BaseModel):
    reason: str = None
    output: str = None
