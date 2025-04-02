from pydantic import BaseModel
from datetime import datetime


class MessageBase(BaseModel):
    sender: str
    content: str


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    timestamp: datetime

    class Config:
        orm_mode = True
