"""AuditLog model - new table for security auditing."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db import Base


class AuditLog(Base):
    """Audit log for tracking user actions."""

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)  # Can be null for failed login attempts
    action = Column(String(100), nullable=False)  # login, logout, update_profile, etc.
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(Text, nullable=True)
    details = Column(Text, nullable=True)  # JSON or text details
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
