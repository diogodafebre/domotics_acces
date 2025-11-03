"""User model - maps to existing 'users' table."""
from datetime import date, datetime

from sqlalchemy import CHAR, Column, DateTime, Integer, String, Date
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    """User model mapping to existing 'users' table."""

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(80), nullable=False)
    prenom = Column(String(80), nullable=False)
    date_naissance = Column(Date, nullable=False)
    rue = Column(String(120), nullable=False)
    npa = Column(CHAR(4), nullable=False)
    localite = Column(String(80), nullable=False)
    tel = Column(String(24), nullable=True)
    email = Column(String(254), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationships
    acces = relationship("AccesApp", back_populates="user", uselist=False, cascade="all, delete")
    abonnements = relationship("Abonnement", back_populates="user", cascade="all, delete")
