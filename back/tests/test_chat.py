from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_valid_chat_history():
    response = client.post("/chat/", json={
        "history": [
            {"sender": "user", "content": "Bonjour"},
            {"sender": "agent", "content": "Salut"},
            {"sender": "user", "content": "comment tu vas ?"}
        ]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["sender"] == "agent"
    assert isinstance(data["content"], str)

def test_invalid_double_user_history():
    response = client.post("/chat/", json={
        "history": [
            {"sender": "user", "content": "coucou"},
            {"sender": "user", "content": "encore moi"}
        ]
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid chat history"

def test_empty_message_content():
    response = client.post("/chat/", json={
        "history": [
            {"sender": "user", "content": ""}
        ]
    })

    assert response.status_code == 422
