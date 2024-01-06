from pydantic import BaseModel
from typing import List


class Input(BaseModel):
    input: str = None


class Output(BaseModel):
    output: str = None
    reason: str = None


class Register(BaseModel):

    string_id: str = None
    date: str = None
    inputs: List[Input] = []
    outputs: List[Output] = []
    modified: bool = False
    nightShift: bool = False
