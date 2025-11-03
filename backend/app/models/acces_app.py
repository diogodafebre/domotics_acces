"""AccesApp model - maps to existing 'acces_app' table."""
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db import Base


class AccesApp(Base):
    """AccesApp model mapping to existing 'acces_app' table."""

    __tablename__ = "acces_app"

    email = Column(
        String(254),
        ForeignKey("users.email", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    password_hash = Column(String(255), nullable=False)

    # Relationships
    user = relationship("User", back_populates="acces")
