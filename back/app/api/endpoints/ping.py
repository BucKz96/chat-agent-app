"""
Health check endpoints for monitoring and Docker health checks.
"""

from datetime import datetime

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/")
async def ping() -> dict:
    """
    Basic health check endpoint.
    Returns service status and version information.
    """
    return {
        "status": "OK",
        "message": "pong",
        "timestamp": datetime.now().isoformat(),
        "service": "chat-agent-backend",
        "version": "1.1.0",
        "environment": get_settings().LOG_LEVEL,
    }


@router.get("/health")
async def health() -> dict:
    """
    Detailed health check including database connectivity.
    """
    from app.services.chat_service import DB_PATH

    db_status = "OK" if DB_PATH.exists() else "ERROR"

    return {
        "status": "healthy" if db_status == "OK" else "unhealthy",
        "database": db_status,
        "timestamp": datetime.now().isoformat(),
    }
