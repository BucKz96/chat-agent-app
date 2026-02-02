"""
Logging configuration for the application.
"""

import logging
import sys

from app.core.config import get_settings


def setup_logging() -> logging.Logger:
    """Configure application logging."""
    settings = get_settings()

    # Create logger
    logger = logging.getLogger("chat_agent")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logging()
