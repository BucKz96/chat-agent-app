"""
Pydantic models for message structure and chat request validation.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints


class Message(BaseModel):
    """
    Represents a message from either 'user' or 'agent'.
    """

    sender: Literal["user", "agent"]
    content: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)] = Field(
        ..., description="Content must not be empty"
    )


class ChatRequest(BaseModel):
    """
    Payload containing the full chat history to validate and process.
    """

    history: list[Message]
