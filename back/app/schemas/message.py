"""
Pydantic models for message structure and chat request validation.
"""

from pydantic import BaseModel, Field, constr
from typing import Literal


class Message(BaseModel):
    """
    Represents a message from either 'user' or 'agent'.
    """

    sender: Literal["user", "agent"]
    content: constr(strip_whitespace=True, min_length=1) = Field(..., description="Content must not be empty")


class ChatRequest(BaseModel):
    """
    Payload containing the full chat history to validate and process.
    """

    history: list[Message]
