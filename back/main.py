from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Literal

app = FastAPI()


class Message(BaseModel):
    role: Literal["user", "agent"]
    content: str


class ChatRequest(BaseModel):
    history: List[Message]


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    history = request.history

    for i in range(1, len(history)):
        if history[i].role == history[i-1].role:
            raise HTTPException(status_code=400, detail="Invalid message sequence")

    return ChatResponse(reply="This is a static agent response.")
