"""
Unit tests for the /chat/ endpoint using FastAPI's TestClient.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_valid_chat_history():
    """
    Test that a valid alternating user/agent message history
    returns an agent response.
    """
    response = client.post(
        "/chat/",
        json={
            "history": [
                {"sender": "user", "content": "Hey"},
                {"sender": "agent", "content": "Hello"},
                {"sender": "user", "content": "What's up ?"},
            ]
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["sender"] == "agent"
    assert isinstance(data["content"], str)


def test_invalid_double_user_history():
    """
    Test that an invalid sequence
    (e.g., two user messages in a row) returns 400.
    """
    response = client.post(
        "/chat/",
        json={
            "history": [
                {"sender": "user", "content": "coucou"},
                {"sender": "user", "content": "encore moi"},
            ]
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid chat history"


def test_empty_message_content():
    response = client.post(
        "/chat/", json={"history": [{"sender": "user", "content": ""}]}
    )

    assert response.status_code == 422
