from pydantic import BaseModel
from typing import Optional


class Schema(BaseModel):

    class Config:
        orm_mode = True


class Bird(Schema):
    uid: int
    name: str
    type: int
    was_fitted: Optional[int]
