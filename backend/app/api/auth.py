"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import AccesApp, User
from app.schemas.auth import LoginRequest, LoginResponse, RefreshRequest, RefreshResponse, UserInfo
from app.schemas.user import UserBasic
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with email and password.

    Steps:
    1. Find user in acces_app by email
    2. Verify bcrypt password
    3. Get user profile from users table
    4. Return JWT tokens + user info
    """
    # 1. Find credentials in acces_app
    acces = db.query(AccesApp).filter(AccesApp.email == credentials.email).first()
    if not acces:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 2. Verify password
    if not verify_password(credentials.password, acces.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 3. Get user profile from users table
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # 4. Create JWT tokens
    access_token = create_access_token(user.user_id, user.email or credentials.email)
    refresh_token = create_refresh_token(user.user_id, user.email or credentials.email)

    # 5. Return response
    return LoginResponse(
        access=access_token,
        refresh=refresh_token,
        user=UserInfo(
            id=user.user_id,
            email=user.email or credentials.email,
            prenom=user.prenom,
            nom=user.nom
        )
    )


@router.post("/refresh", response_model=RefreshResponse)
def refresh(request: RefreshRequest):
    """
    Refresh access token using refresh token.

    Verifies the refresh token and returns a new access token.
    """
    # Decode and verify refresh token
    payload = decode_token(request.refresh)

    # Check token type
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    user_id = payload.get("sub")
    email = payload.get("email")

    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    # Create new access token
    new_access_token = create_access_token(int(user_id), email)

    return RefreshResponse(access=new_access_token)


@router.get("/me", response_model=UserBasic)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user information.

    Requires valid Bearer access token.
    """
    return UserBasic(
        id=current_user.user_id,
        email=current_user.email,
        prenom=current_user.prenom,
        nom=current_user.nom
    )
