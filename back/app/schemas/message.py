from pydantic import BaseModel, validator
from datetime import datetime
from typing import Literal


class Message(BaseModel):
    sender: Literal["user", "agent"]
    content: str

    @validator("content")
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("content must not be empty")
        return v


class ChatRequest(BaseModel):
    history: list[Message]


class MessageCreate(Message):
    pass


class MessageResponse(Message):
    timestamp: datetime

    class Config:
        orm_mode = True
