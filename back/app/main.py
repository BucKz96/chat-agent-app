"""
Main application entrypoint for the FastAPI backend.
Initializes routes, API structure, logging and error handling.
"""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.endpoints import chat, ping
from app.core.config import get_settings
from app.core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    settings = get_settings()
    logger.info(f"Starting Chat Agent API v1.1.0 on {settings.API_HOST}:{settings.API_PORT}")
    logger.info(f"Frontend URL configured: {settings.FRONTEND_URL}")
    yield
    # Shutdown
    logger.info("Shutting down Chat Agent API")


# Initialize FastAPI application with metadata
app = FastAPI(
    title="Chat Agent API",
    description="Simple chat application API with user-agent conversation support",
    version="1.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Get settings
settings = get_settings()

# Configure CORS with environment variable
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and their processing time."""
    start_time = time.time()

    # Log request
    logger.info(f"{request.method} {request.url.path} - Request received")

    # Process request
    response = await call_next(request)

    # Log response
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Response {response.status_code} ({process_time:.3f}s)"
    )

    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions globally."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# Include routers
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(ping.router, prefix="/ping", tags=["system"])
