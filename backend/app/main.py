"""FastAPI application entry point."""
import logging

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import settings
from app.db import close_redis, init_redis
from app.routers import auth, users, ws
from app.utils.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Move Acces API",
    description="Backend API for Move Acces mobile application",
    version="1.0.0",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "code": "INTERNAL_ERROR"},
    )


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize connections on startup."""
    logger.info("Starting Move Acces API...")
    await init_redis()
    logger.info("Redis connection established")

    # Initialize Prometheus metrics
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
    logger.info("Prometheus metrics enabled at /metrics")


@app.on_event("shutdown")
async def shutdown_event():
    """Close connections on shutdown."""
    logger.info("Shutting down Move Acces API...")
    await close_redis()
    logger.info("Redis connection closed")


# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ws.router)


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "environment": settings.environment}


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "Move Acces API",
        "version": "1.0.0",
        "docs": "/docs" if not settings.is_production else "disabled",
    }
