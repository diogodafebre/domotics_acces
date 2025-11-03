"""JWT token generation and validation."""
from datetime import datetime, timedelta
from typing import Dict, Optional

from jose import JWTError, jwt

from app.config import settings


def create_access_token(data: Dict[str, str]) -> str:
    """Create JWT access token.

    Args:
        data: Data to encode in token (typically {"sub": email})

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_ttl_min)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.app_secret, algorithm=settings.algorithm)


def create_refresh_token(data: Dict[str, str]) -> str:
    """Create JWT refresh token.

    Args:
        data: Data to encode in token (typically {"sub": email})

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=settings.refresh_token_ttl_hours)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.app_secret, algorithm=settings.algorithm)


def decode_access_token(token: str) -> Optional[Dict[str, str]]:
    """Decode and validate access token.

    Args:
        token: JWT token to decode

    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.app_secret, algorithms=[settings.algorithm])
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
        return None


def decode_refresh_token(token: str) -> Optional[Dict[str, str]]:
    """Decode and validate refresh token.

    Args:
        token: JWT token to decode

    Returns:
        Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(token, settings.app_secret, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            return None
        return payload
    except JWTError:
        return None
