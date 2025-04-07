"""
Chat endpoint - handles the POST /chat/ route logic.
"""

from fastapi import APIRouter, HTTPException
from app.schemas.message import ChatRequest, Message
from app.services.chat_service import (is_valid_chat_history,
                                       generate_agent_reply)

# Create a router for chat endpoints
router = APIRouter()


@router.post("/chat/", response_model=Message)
async def chat(chat_request: ChatRequest):
    """
    Processes a chat request and returns the agent's response.
    Validates the message history to ensure proper alternance.
    """
    if not is_valid_chat_history(chat_request.history):
        raise HTTPException(status_code=400, detail="Invalid chat history")

    return generate_agent_reply(chat_request.history)
