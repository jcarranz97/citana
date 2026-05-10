from datetime import UTC, datetime, timedelta


def future_iso(hours: int = 24) -> str:
    """Return an ISO-8601 datetime string `hours` from now (UTC)."""
    return (datetime.now(UTC) + timedelta(hours=hours)).isoformat()
