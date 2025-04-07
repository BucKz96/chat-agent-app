"""
Chat service layer: handles validation and agent response generation logic.
"""

from app.schemas.message import Message


def is_valid_chat_history(history: list[Message]) -> bool:
    """
    Validates that the message history alternates between user and agent.
    """
    if not history:
        return False
    expected_sender = "user"
    for msg in history:
        if msg.sender != expected_sender:
            return False
        expected_sender = "agent" if expected_sender == "user" else "user"
    return True


def generate_agent_reply() -> Message:
    """
    Generates a default response from the agent.
    """
    return Message(sender="agent", content="Ceci est une réponse automatique.")
