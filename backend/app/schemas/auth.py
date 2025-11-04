"""Pydantic schemas for authentication."""
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Login request with email and password."""
    email: EmailStr
    password: str


class UserInfo(BaseModel):
    """User information returned in auth responses."""
    id: int
    email: str
    prenom: str | None = None
    nom: str | None = None

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Login response with JWT tokens and user info."""
    access: str
    refresh: str
    user: UserInfo


class RefreshRequest(BaseModel):
    """Refresh token request."""
    refresh: str


class RefreshResponse(BaseModel):
    """Refresh token response with new access token."""
    access: str
