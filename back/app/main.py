"""
Main application entrypoint for the FastAPI backend.
Initializes routes and API structure.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import chat, ping

# Initialize FastAPI application
app = FastAPI()

# Include router for each endpoints
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(ping.router, prefix="/ping", tags=["ping"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Front local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
