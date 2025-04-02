from app.schemas.message import Message, ChatRequest


def is_valid_chat_history(history: list[Message]) -> bool:
    if not history:
        return False
    expected_sender = "user"
    for msg in history:
        if msg.sender != expected_sender:
            return False
        expected_sender = "agent" if expected_sender == "user" else "user"
    return True


def generate_agent_reply(history: list[Message]) -> Message:

    return Message(sender="agent", content="Ceci est une réponse automatique.")
