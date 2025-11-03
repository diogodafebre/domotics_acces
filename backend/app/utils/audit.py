"""Audit logging utilities."""
from typing import Optional

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.utils.rate_limit import get_client_ip


async def log_audit(
    db: AsyncSession,
    action: str,
    user_id: Optional[int] = None,
    request: Optional[Request] = None,
    details: Optional[str] = None,
) -> None:
    """Log an audit event.

    Args:
        db: Database session
        action: Action performed (e.g., "login", "logout", "update_profile")
        user_id: User ID if authenticated
        request: FastAPI request object
        details: Additional details as string or JSON
    """
    ip_address = None
    user_agent = None

    if request:
        ip_address = get_client_ip(request)
        user_agent = request.headers.get("User-Agent")

    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        ip_address=ip_address,
        user_agent=user_agent,
        details=details,
    )

    db.add(audit_log)
    await db.commit()
