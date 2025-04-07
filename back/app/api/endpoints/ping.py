from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/ping")
async def ping():
    return {
        "status": "OK",
        "message": "pong",
        "timestamp": datetime.now().isoformat(),
        "service": "chat-agent-backend",
        "version": "1.0.0"
    }


