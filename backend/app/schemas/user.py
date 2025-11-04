"""Pydantic schemas for user data."""
from datetime import date
from pydantic import BaseModel, EmailStr


class UserProfile(BaseModel):
    """Complete user profile information."""
    id: int
    email: str | None = None
    nom: str | None = None
    prenom: str | None = None
    date_naissance: date | None = None
    rue: str | None = None
    npa: str | None = None
    localite: str | None = None
    tel: str | None = None

    class Config:
        from_attributes = True


class UserBasic(BaseModel):
    """Basic user information for /me endpoint."""
    id: int
    email: str | None = None
    prenom: str | None = None
    nom: str | None = None

    class Config:
        from_attributes = True
