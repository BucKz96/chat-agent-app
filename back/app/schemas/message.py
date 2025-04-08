"""
Pydantic models for message structure and chat request validation.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class Message(BaseModel):
    """
    Represents a message from either 'user' or 'agent'.
    """

    sender: Literal["user", "agent"]
    content: str = Field(...)


    @classmethod
    @field_validator("content", mode='before')
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("content must not be empty")
        return v


class ChatRequest(BaseModel):
    """
    Payload containing the full chat history to validate and process.
    """

    history: list[Message]
