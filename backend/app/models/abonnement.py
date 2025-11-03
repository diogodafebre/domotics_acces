"""Abonnement model - maps to existing 'abonnement' table."""
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    DECIMAL,
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    BIGINT,
    SMALLINT,
)
from sqlalchemy.orm import relationship

from app.db import Base


class Abonnement(Base):
    """Abonnement model mapping to existing 'abonnement' table."""

    __tablename__ = "abonnement"

    abo_id = Column(BIGINT(unsigned=True), primary_key=True, autoincrement=True)
    abo_id_actual = Column(String(64), nullable=True, unique=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    abo_state = Column(
        Enum("active", "paused", "expired", "canceled", "pending", name="abo_state_enum"),
        nullable=False,
        default="pending",
    )
    abo_name = Column(String(80), nullable=False)
    abo_date_start = Column(Date, nullable=True)
    abo_date_creation = Column(DateTime, nullable=False, default=datetime.utcnow)
    abo_date_stop = Column(Date, nullable=True)
    abo_duration = Column(Integer, nullable=True)
    abo_renew = Column(SMALLINT, nullable=False, default=0)
    abo_price = Column(DECIMAL(10, 2), nullable=False, default=Decimal("0.00"))
    abo_discount = Column(DECIMAL(5, 2), nullable=False, default=Decimal("0.00"))
    abo_slices = Column(Integer, nullable=True)
    abo_price_finances = Column(DECIMAL(10, 2), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationships
    user = relationship("User", back_populates="abonnements")
