"""Rate limiting utilities using Redis."""
from typing import Optional

from fastapi import HTTPException, Request, status
from redis.asyncio import Redis

from app.config import settings


async def check_rate_limit(
    redis: Redis,
    key: str,
    max_requests: int,
    window_seconds: int,
    identifier: str = "IP",
) -> None:
    """Check if request is within rate limit.

    Args:
        redis: Redis client
        key: Rate limit key (e.g., "rate_limit:login:192.168.1.1")
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds
        identifier: Identifier type for error message

    Raises:
        HTTPException: If rate limit exceeded
    """
    current = await redis.get(key)

    if current is None:
        # First request in window
        await redis.setex(key, window_seconds, 1)
    else:
        current_int = int(current)
        if current_int >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again later.",
                headers={"Retry-After": str(window_seconds)},
            )
        await redis.incr(key)


def get_client_ip(request: Request) -> str:
    """Get client IP address from request.

    Args:
        request: FastAPI request

    Returns:
        Client IP address
    """
    # Check X-Forwarded-For header (reverse proxy)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()

    # Check X-Real-IP header
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # Fallback to direct client
    return request.client.host if request.client else "unknown"


async def rate_limit_login(redis: Redis, ip: str) -> None:
    """Apply rate limit for login endpoint.

    Args:
        redis: Redis client
        ip: Client IP address

    Raises:
        HTTPException: If rate limit exceeded
    """
    key = f"rate_limit:login:{ip}"
    await check_rate_limit(
        redis,
        key,
        settings.rate_limit_login_per_min,
        60,  # 1 minute window
        "IP",
    )


async def rate_limit_api(redis: Redis, ip: str) -> None:
    """Apply rate limit for general API endpoints.

    Args:
        redis: Redis client
        ip: Client IP address

    Raises:
        HTTPException: If rate limit exceeded
    """
    key = f"rate_limit:api:{ip}"
    await check_rate_limit(
        redis,
        key,
        settings.rate_limit_api_per_5min,
        300,  # 5 minute window
        "IP",
    )
