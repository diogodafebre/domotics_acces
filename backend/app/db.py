"""Database connection and session management."""
import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from app.config import settings

# SQLAlchemy Base
Base = declarative_base()

# Async engine with connection pooling
engine = create_async_engine(
    settings.db_url,
    echo=not settings.is_production,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=True,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Redis client (will be initialized in main.py)
redis_client: aioredis.Redis = None


async def get_db() -> AsyncSession:
    """Dependency to get async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_redis() -> aioredis.Redis:
    """Dependency to get Redis client."""
    return redis_client


async def init_redis():
    """Initialize Redis connection."""
    global redis_client
    redis_client = await aioredis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )


async def close_redis():
    """Close Redis connection."""
    if redis_client:
        await redis_client.close()
