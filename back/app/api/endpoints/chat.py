from fastapi import APIRouter, HTTPException
from app.schemas.message import MessageCreate, MessageResponse
from app.services.chat_service import generate_agent_response

router = APIRouter()


@router.post("/chat/", response_model=MessageResponse)
async def chat_endpoint(user_message: MessageCreate):
    if not user_message.content:
        raise HTTPException(status_code=400, detail="Le message ne peut pas être vide.")
    return generate_agent_response(user_message)
