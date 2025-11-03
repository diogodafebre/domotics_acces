"""Authentication schemas."""
from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    """Registration request."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=80)
    last_name: str = Field(..., min_length=1, max_length=80)
    date_naissance: date
    rue: str = Field(..., min_length=1, max_length=120)
    npa: str = Field(..., min_length=4, max_length=4)
    localite: str = Field(..., min_length=1, max_length=80)
    tel: Optional[str] = Field(None, max_length=24)

    @field_validator("npa")
    @classmethod
    def validate_npa(cls, v: str) -> str:
        """Validate NPA is 4 digits."""
        if not v.isdigit() or len(v) != 4:
            raise ValueError("NPA must be exactly 4 digits")
        return v


class LoginRequest(BaseModel):
    """Login request."""

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: "UserInfo"


class UserInfo(BaseModel):
    """User information included in login response."""

    user_id: int
    email: str
    prenom: str
    nom: str


class RefreshRequest(BaseModel):
    """Refresh token request."""

    refresh_token: str


class RefreshResponse(BaseModel):
    """Refresh token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LogoutRequest(BaseModel):
    """Logout request."""

    refresh_token: str


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str
    code: str
