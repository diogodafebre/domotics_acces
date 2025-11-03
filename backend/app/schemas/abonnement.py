"""Abonnement schemas."""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class AbonnementResponse(BaseModel):
    """Abonnement response schema."""

    abo_id: int
    abo_id_actual: Optional[str]
    user_id: int
    abo_state: str
    abo_name: str
    abo_date_start: Optional[date]
    abo_date_creation: datetime
    abo_date_stop: Optional[date]
    abo_duration: Optional[int]
    abo_renew: int
    abo_price: Decimal
    abo_discount: Decimal
    abo_slices: Optional[int]
    abo_price_finances: Optional[Decimal]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
