"""
Application configuration using environment variables.
"""

import os
from functools import lru_cache

from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:8080")

    # Database
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "./chat.db")

    # Agent Configuration
    AGENT_NAME: str = os.getenv("AGENT_NAME", "Agent")
    MAX_HISTORY_LENGTH: int = int(os.getenv("MAX_HISTORY_LENGTH", "50"))


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
