"""
Chat endpoints - handles chat routes and message history.
"""

from fastapi import APIRouter, HTTPException, Query

from app.core.logging import logger
from app.schemas.message import ChatRequest, Message
from app.services.chat_service import (
    is_valid_chat_history,
    generate_agent_reply,
    save_message,
    get_recent_messages,
    clear_history,
)

# Create a router for chat endpoints
router = APIRouter()


@router.post("/", response_model=Message)
async def chat(chat_request: ChatRequest):
    """
    Process a chat request and return the agent's contextual response.
    Validates the message history and persists messages to database.
    """
    logger.info(f"Received chat request with {len(chat_request.history)} messages")

    # Validate chat history
    if not is_valid_chat_history(chat_request.history):
        logger.warning("Chat request rejected: invalid history")
        raise HTTPException(status_code=400, detail="Invalid chat history")

    # Save user message to database
    if chat_request.history:
        last_message = chat_request.history[-1]
        if last_message.sender == "user":
            save_message(last_message)

    # Generate contextual agent response
    try:
        agent_reply = generate_agent_reply(chat_request.history)
        logger.info(f"Generated agent response: {agent_reply.content[:50]}...")

        # Save agent response to database
        save_message(agent_reply)

        return agent_reply
    except Exception as e:
        logger.error(f"Error generating agent reply: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate response")


@router.get("/history", response_model=list[Message])
async def get_history(limit: int = Query(50, ge=1, le=100)):
    """
    Retrieve recent chat history from database.
    """
    logger.info(f"Retrieving chat history (limit: {limit})")
    messages = get_recent_messages(limit)
    return messages


@router.delete("/history")
async def delete_history():
    """
    Clear all chat history from database.
    """
    logger.info("Clearing chat history")
    clear_history()
    return {"message": "Chat history cleared successfully"}
