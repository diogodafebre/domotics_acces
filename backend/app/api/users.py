"""User endpoints (future expansion)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User
from app.schemas.user import UserProfile
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/profile", response_model=UserProfile)
def get_profile(current_user: User = Depends(get_current_user)):
    """Get complete user profile (future expansion)."""
    return UserProfile(
        id=current_user.user_id,
        email=current_user.user_email,
        nom=current_user.user_nom,
        prenom=current_user.user_prenom,
        date_naissance=current_user.user_date_naissance,
        rue=current_user.user_rue,
        npa=current_user.user_npa,
        localite=current_user.user_localite,
        telephone=current_user.user_telephone,
        mobile=current_user.user_mobile
    )
