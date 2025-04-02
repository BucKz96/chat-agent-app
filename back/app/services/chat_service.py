from app.schemas.message import MessageCreate, MessageResponse


def generate_agent_response(user_message: MessageCreate) -> MessageResponse:

    response_content = "Ceci est une réponse statique de l'agent."
    return MessageResponse(sender="agent", content=response_content, timestamp=datetime.utcnow())
