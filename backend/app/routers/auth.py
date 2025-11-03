"""Authentication router."""
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Request, status
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import get_db, get_redis
from app.models.acces_app import AccesApp
from app.models.user import User
from app.schemas.auth import (
    ErrorResponse,
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    RefreshRequest,
    RefreshResponse,
    RegisterRequest,
    UserInfo,
)
from app.security.passwords import hash_password, verify_password
from app.security.tokens import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.utils.audit import log_audit
from app.utils.rate_limit import get_client_ip, rate_limit_login

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInfo,
    responses={
        400: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def register(
    request: Request,
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> UserInfo:
    """Register a new user.

    Creates a new user account with credentials.
    """
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    # Create user
    user = User(
        email=data.email,
        prenom=data.first_name,
        nom=data.last_name,
        date_naissance=data.date_naissance,
        rue=data.rue,
        npa=data.npa,
        localite=data.localite,
        tel=data.tel,
    )
    db.add(user)
    await db.flush()

    # Create access credentials
    password_hash_str = hash_password(data.password)
    acces = AccesApp(email=data.email, password_hash=password_hash_str)
    db.add(acces)

    await db.commit()
    await db.refresh(user)

    # Log audit
    await log_audit(db, "register", user.user_id, request)

    return UserInfo(
        user_id=user.user_id,
        email=user.email,
        prenom=user.prenom,
        nom=user.nom,
    )


@router.post(
    "/login",
    response_model=LoginResponse,
    responses={
        401: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
    },
)
async def login(
    request: Request,
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> LoginResponse:
    """Login with email and password.

    Returns access token, refresh token, and user information.
    """
    # Rate limiting
    ip = get_client_ip(request)
    await rate_limit_login(redis, ip)

    # Fetch user credentials
    result = await db.execute(select(AccesApp).where(AccesApp.email == data.email))
    acces = result.scalar_one_or_none()

    if not acces or not verify_password(data.password, acces.password_hash):
        # Log failed attempt
        await log_audit(db, "login_failed", None, request, f"Email: {data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    # Fetch user details
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Generate tokens
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})

    # Log successful login
    await log_audit(db, "login", user.user_id, request)

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.access_token_ttl_min * 60,
        user=UserInfo(
            user_id=user.user_id,
            email=user.email,
            prenom=user.prenom,
            nom=user.nom,
        ),
    )


@router.post(
    "/refresh",
    response_model=RefreshResponse,
    responses={
        401: {"model": ErrorResponse},
    },
)
async def refresh(
    data: RefreshRequest,
    redis: Redis = Depends(get_redis),
) -> RefreshResponse:
    """Refresh access token using refresh token."""
    # Decode refresh token
    payload = decode_refresh_token(data.refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    # Check if token is blacklisted
    blacklisted = await redis.get(f"blacklist:{data.refresh_token}")
    if blacklisted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked",
        )

    # Generate new access token
    access_token = create_access_token({"sub": email})

    return RefreshResponse(
        access_token=access_token,
        expires_in=settings.access_token_ttl_min * 60,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        401: {"model": ErrorResponse},
    },
)
async def logout(
    request: Request,
    data: LogoutRequest,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> None:
    """Logout user and invalidate refresh token."""
    # Decode refresh token to get user info
    payload = decode_refresh_token(data.refresh_token)

    # Blacklist the refresh token (TTL = refresh token lifetime)
    ttl = settings.refresh_token_ttl_hours * 3600
    await redis.setex(f"blacklist:{data.refresh_token}", ttl, "1")

    # Log audit if we can identify the user
    if payload and payload.get("sub"):
        email = payload["sub"]
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if user:
            await log_audit(db, "logout", user.user_id, request)
