"""
ISMAIL AI - Computer Context Lifecycle
Task 14F-F
Logical lifecycle policy for persistent computer context.
IMPORTANT:
This module only evaluates stored logical context age.
It does NOT inspect or modify the real computer.
It does NOT execute computer actions.
"""
from datetime import datetime, timezone
from typing import Optional
ACTIVE_MAX_DAYS = 30
STALE_MAX_DAYS = 90
LIFECYCLE_ACTIVE = "active"
LIFECYCLE_STALE = "stale"
LIFECYCLE_EXPIRED = "expired"
VALID_LIFECYCLE_STATES = {
    LIFECYCLE_ACTIVE,
    LIFECYCLE_STALE,
    LIFECYCLE_EXPIRED,
}
def utc_now_iso() -> str:
    """
    Return the current UTC time as an ISO-8601 string.
    """
    return datetime.now(timezone.utc).isoformat()
def parse_timestamp(value: Optional[str]) -> Optional[datetime]:
    """
    Parse an ISO-8601 timestamp safely.
    Invalid timestamps return None.
    """
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)
def calculate_age_days(
    timestamp: Optional[str],
    now: Optional[datetime] = None,
) -> Optional[float]:
    """
    Calculate logical age in days from a stored timestamp.
    """
    parsed = parse_timestamp(timestamp)
    if parsed is None:
        return None
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    current = current.astimezone(timezone.utc)
    age_seconds = max(
        0.0,
        (current - parsed).total_seconds(),
    )
    return age_seconds / 86400.0
def get_lifecycle_status(
    updated_at: Optional[str],
    now: Optional[datetime] = None,
) -> str:
    """
    Determine lifecycle state from the logical update timestamp.
    Missing or invalid timestamps are treated as ACTIVE
    so legacy states remain usable and are not accidentally
    destroyed because of missing metadata.
    """
    age_days = calculate_age_days(
        updated_at,
        now=now,
    )
    if age_days is None:
        return LIFECYCLE_ACTIVE
    if age_days < ACTIVE_MAX_DAYS:
        return LIFECYCLE_ACTIVE
    if age_days < STALE_MAX_DAYS:
        return LIFECYCLE_STALE
    return LIFECYCLE_EXPIRED
def is_stale(
    updated_at: Optional[str],
    now: Optional[datetime] = None,
) -> bool:
    return get_lifecycle_status(
        updated_at,
        now=now,
    ) == LIFECYCLE_STALE
def is_expired(
    updated_at: Optional[str],
    now: Optional[datetime] = None,
) -> bool:
    return get_lifecycle_status(
        updated_at,
        now=now,
    ) == LIFECYCLE_EXPIRED
def is_active(
    updated_at: Optional[str],
    now: Optional[datetime] = None,
) -> bool:
    return get_lifecycle_status(
        updated_at,
        now=now,
    ) == LIFECYCLE_ACTIVE
def can_transition(
    current_status: str,
    new_status: str,
) -> bool:
    """
    Enforce monotonic expiration.
    ACTIVE -> ACTIVE/STALE/EXPIRED
    STALE  -> STALE/EXPIRED
    EXPIRED -> EXPIRED
    """
    current = str(
        current_status or LIFECYCLE_ACTIVE
    ).strip().lower()
    new = str(
        new_status or LIFECYCLE_ACTIVE
    ).strip().lower()
    if current not in VALID_LIFECYCLE_STATES:
        return False
    if new not in VALID_LIFECYCLE_STATES:
        return False
    allowed = {
        LIFECYCLE_ACTIVE: {
            LIFECYCLE_ACTIVE,
            LIFECYCLE_STALE,
            LIFECYCLE_EXPIRED,
        },
        LIFECYCLE_STALE: {
            LIFECYCLE_STALE,
            LIFECYCLE_EXPIRED,
        },
        LIFECYCLE_EXPIRED: {
            LIFECYCLE_EXPIRED,
        },
    }
    return new in allowed[current]
