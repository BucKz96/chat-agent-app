"""
Unit tests for the chat endpoints using FastAPI's TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestChatEndpoint:
    """Tests for the main chat endpoint."""

    def test_valid_chat_history(self):
        """Test that a valid alternating user/agent message history returns an agent response."""
        response = client.post(
            "/chat/",
            json={
                "history": [
                    {"sender": "user", "content": "Hey"},
                    {"sender": "agent", "content": "Hello"},
                    {"sender": "user", "content": "What's up?"},
                ]
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["sender"] == "agent"
        assert isinstance(data["content"], str)
        assert len(data["content"]) > 0

    def test_first_message_from_user(self):
        """Test that the first message can be from user (empty history)."""
        response = client.post(
            "/chat/",
            json={
                "history": [
                    {"sender": "user", "content": "Hello"},
                ]
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["sender"] == "agent"
        assert "content" in data

    def test_invalid_double_user_history(self):
        """Test that two user messages in a row returns 400."""
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
        assert "detail" in response.json()

    def test_empty_history(self):
        """Test that empty history returns 400."""
        response = client.post(
            "/chat/",
            json={"history": []},
        )

        assert response.status_code == 400

    def test_empty_message_content(self):
        """Test that empty message content returns 422 (validation error)."""
        response = client.post(
            "/chat/",
            json={"history": [{"sender": "user", "content": ""}]},
        )

        assert response.status_code == 422

    def test_whitespace_only_content(self):
        """Test that whitespace-only content is rejected."""
        response = client.post(
            "/chat/",
            json={"history": [{"sender": "user", "content": "   "}]},
        )

        assert response.status_code == 422


class TestChatHistory:
    """Tests for chat history endpoints."""

    def test_get_history_empty(self):
        """Test retrieving history when no messages exist."""
        # Clear history first
        client.delete("/chat/history")

        response = client.get("/chat/history")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_history_with_messages(self):
        """Test retrieving history after sending messages."""
        # First send a message
        client.post(
            "/chat/",
            json={"history": [{"sender": "user", "content": "Test message"}]},
        )

        response = client.get("/chat/history")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2  # User message + agent response
        assert all("sender" in msg and "content" in msg for msg in data)

    def test_clear_history(self):
        """Test clearing chat history."""
        # First add a message
        client.post(
            "/chat/",
            json={"history": [{"sender": "user", "content": "Test"}]},
        )

        # Clear history
        response = client.delete("/chat/history")
        assert response.status_code == 200
        assert "cleared" in response.json()["message"].lower()

        # Verify it's empty
        history_response = client.get("/chat/history")
        assert history_response.json() == []

    def test_history_limit(self):
        """Test that history endpoint respects limit parameter."""
        response = client.get("/chat/history?limit=5")
        assert response.status_code == 200
        assert len(response.json()) <= 5


class TestPingEndpoint:
    """Tests for the ping/health endpoints."""

    def test_ping(self):
        """Test basic ping endpoint."""
        response = client.get("/ping/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "OK"
        assert data["message"] == "pong"
        assert "timestamp" in data
        assert "version" in data

    def test_health(self):
        """Test detailed health endpoint."""
        response = client.get("/ping/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "unhealthy"]
        assert "database" in data
        assert "timestamp" in data


class TestContextualResponses:
    """Tests for contextual agent responses."""

    def test_greeting_response(self):
        """Test agent responds appropriately to greetings."""
        response = client.post(
            "/chat/",
            json={"history": [{"sender": "user", "content": "Bonjour"}]},
        )

        data = response.json()
        assert "bonjour" in data["content"].lower() or "ravi" in data["content"].lower()

    def test_thanks_response(self):
        """Test agent responds appropriately to thanks."""
        response = client.post(
            "/chat/",
            json={"history": [{"sender": "user", "content": "Merci"}]},
        )

        data = response.json()
        assert (
            "je vous en prie" in data["content"].lower() or "pas de quoi" in data["content"].lower()
        )

    def test_help_response(self):
        """Test agent responds appropriately to help requests."""
        response = client.post(
            "/chat/",
            json={"history": [{"sender": "user", "content": "J'ai besoin d'aide"}]},
        )

        data = response.json()
        assert "aider" in data["content"].lower()
