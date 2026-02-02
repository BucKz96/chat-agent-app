"""
Chat service layer: handles validation, persistence and agent response generation logic.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

from app.core.config import get_settings
from app.core.logging import logger
from app.schemas.message import Message


# Initialize database on module load
settings = get_settings()
DB_PATH = Path(settings.DATABASE_PATH)


def init_db():
    """Initialize SQLite database with messages table."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    logger.info(f"Database initialized at {DB_PATH}")


def save_message(message: Message) -> int:
    """Save a message to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (sender, content) VALUES (?, ?)", (message.sender, message.content)
    )

    message_id = cursor.lastrowid or 0
    conn.commit()
    conn.close()

    logger.info(f"Message saved: {message.sender} - {message_id}")
    return message_id


def get_recent_messages(limit: int | None = None) -> list[Message]:
    """Retrieve recent messages from database."""
    limit = limit if limit is not None else get_settings().MAX_HISTORY_LENGTH

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT sender, content FROM messages ORDER BY timestamp DESC LIMIT ?", (limit,))

    rows = cursor.fetchall()
    conn.close()

    # Reverse to get chronological order
    messages = [Message(sender=row[0], content=row[1]) for row in reversed(rows)]
    return messages


def clear_history():
    """Clear all message history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    logger.info("Chat history cleared")


def is_valid_chat_history(history: list[Message]) -> bool:
    """
    Validates that the message history alternates between user and agent.
    """
    if not history:
        logger.warning("Empty chat history received")
        return False

    expected_sender = "user"
    for i, msg in enumerate(history):
        if msg.sender != expected_sender:
            logger.warning(
                f"Invalid sequence at position {i}: expected {expected_sender}, got {msg.sender}"
            )
            return False
        expected_sender = "agent" if expected_sender == "user" else "user"

    logger.info(f"Chat history validated: {len(history)} messages")
    return True


def generate_agent_reply(history: list[Message] | None = None) -> Message:
    """
    Generates a contextual response from the agent based on conversation history.

    This is a simple rule-based agent that responds contextually to common greetings
    and questions. In a real application, this would connect to an LLM API.
    """
    settings = get_settings()

    if not history:
        # First message - greeting
        return Message(
            sender="agent",
            content=f"Bonjour ! Je suis {settings.AGENT_NAME}. Comment puis-je vous aider aujourd'hui ?",
        )

    # Get last user message
    last_user_msg = history[-1].content.lower()

    # Simple contextual responses
    if any(word in last_user_msg for word in ["bonjour", "salut", "hello", "coucou"]):
        return Message(
            sender="agent", content="Bonjour ! Ravie de vous revoir. Que puis-je faire pour vous ?"
        )
    elif any(word in last_user_msg for word in ["merci", "thanks", "thx"]):
        return Message(
            sender="agent",
            content="Je vous en prie ! N'hésitez pas si vous avez d'autres questions.",
        )
    elif any(word in last_user_msg for word in ["aide", "help", "assistance"]):
        return Message(
            sender="agent",
            content="Je suis là pour vous aider ! Vous pouvez me poser des questions ou discuter.",
        )
    elif any(word in last_user_msg for word in ["au revoir", "bye", "ciao"]):
        return Message(sender="agent", content="Au revoir ! Passez une excellente journée !")
    elif "?" in last_user_msg:
        return Message(
            sender="agent",
            content="C'est une question intéressante ! Je suis un agent simple, mais je fais de mon mieux pour vous aider.",
        )
    else:
        # Default contextual response
        return Message(
            sender="agent",
            content="J'ai bien reçu votre message. Que puis-je faire d'autre pour vous aider ?",
        )


# Initialize database on import
init_db()
