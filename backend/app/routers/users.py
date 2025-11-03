"""Users router."""
from fastapi import APIRouter, Depends, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db, get_redis
from app.deps import get_current_user
from app.models.user import User
from app.schemas.auth import ErrorResponse
from app.schemas.user import UserResponse, UserUpdateRequest
from app.utils.audit import log_audit
from app.utils.rate_limit import get_client_ip, rate_limit_api

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        401: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
    },
)
async def get_current_user_profile(
    request: Request,
    current_user: User = Depends(get_current_user),
    redis: Redis = Depends(get_redis),
) -> UserResponse:
    """Get current user profile.

    Returns the authenticated user's profile information.
    """
    # Rate limiting
    ip = get_client_ip(request)
    await rate_limit_api(redis, ip)

    return UserResponse.model_validate(current_user)


@router.patch(
    "/me",
    response_model=UserResponse,
    responses={
        401: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
    },
)
async def update_current_user_profile(
    request: Request,
    data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> UserResponse:
    """Update current user profile.

    Updates the authenticated user's profile information.
    """
    # Rate limiting
    ip = get_client_ip(request)
    await rate_limit_api(redis, ip)

    # Update fields if provided
    if data.first_name is not None:
        current_user.prenom = data.first_name
    if data.last_name is not None:
        current_user.nom = data.last_name
    if data.rue is not None:
        current_user.rue = data.rue
    if data.npa is not None:
        current_user.npa = data.npa
    if data.localite is not None:
        current_user.localite = data.localite
    if data.tel is not None:
        current_user.tel = data.tel

    await db.commit()
    await db.refresh(current_user)

    # Log audit
    await log_audit(db, "update_profile", current_user.user_id, request)

    return UserResponse.model_validate(current_user)
