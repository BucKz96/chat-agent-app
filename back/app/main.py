from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import chat, ping

app = FastAPI()

app.include_router(chat.router)
app.include_router(ping.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Front local
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


