"""User schemas."""
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    prenom: str
    nom: str


class UserResponse(BaseModel):
    """User response schema."""

    user_id: int
    email: str
    prenom: str
    nom: str
    date_naissance: date
    rue: str
    npa: str
    localite: str
    tel: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserUpdateRequest(BaseModel):
    """User update request."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=80)
    last_name: Optional[str] = Field(None, min_length=1, max_length=80)
    rue: Optional[str] = Field(None, min_length=1, max_length=120)
    npa: Optional[str] = Field(None, min_length=4, max_length=4)
    localite: Optional[str] = Field(None, min_length=1, max_length=80)
    tel: Optional[str] = Field(None, max_length=24)
