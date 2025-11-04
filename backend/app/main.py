"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, users

# Create FastAPI application
app = FastAPI(
    title="Domotics Access API",
    description="Authentication API for Domotics mobile app",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Domotics Access API v1.0"}


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}
