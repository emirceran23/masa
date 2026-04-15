"""Redis client wrapper for session, cache, and rate-limiting."""

import redis.asyncio as aioredis

from app.config import settings

redis_client = aioredis.from_url(
    settings.redis_url,
    decode_responses=True,
)


async def get_redis() -> aioredis.Redis:
    return redis_client


# ── Login attempt tracking ───────────────────────────────
LOGIN_ATTEMPT_PREFIX = "login_attempts:"
LOGIN_LOCK_PREFIX = "login_lock:"


async def increment_login_attempts(email: str) -> int:
    """Increment failed login counter; returns current count."""
    key = f"{LOGIN_ATTEMPT_PREFIX}{email}"
    count = await redis_client.incr(key)
    if count == 1:
        await redis_client.expire(key, settings.LOGIN_LOCKOUT_MINUTES * 60)
    return count


async def is_account_locked(email: str) -> bool:
    key = f"{LOGIN_LOCK_PREFIX}{email}"
    return await redis_client.exists(key) == 1


async def lock_account(email: str) -> None:
    key = f"{LOGIN_LOCK_PREFIX}{email}"
    await redis_client.setex(key, settings.LOGIN_LOCKOUT_MINUTES * 60, "locked")
    # clear the counter
    await redis_client.delete(f"{LOGIN_ATTEMPT_PREFIX}{email}")


async def clear_login_attempts(email: str) -> None:
    await redis_client.delete(f"{LOGIN_ATTEMPT_PREFIX}{email}")


# ── Analysis progress ────────────────────────────────────
ANALYSIS_PREFIX = "analysis:"


async def set_analysis_progress(contract_id: str, data: dict) -> None:
    import json

    key = f"{ANALYSIS_PREFIX}{contract_id}"
    await redis_client.setex(key, 3600, json.dumps(data))


async def get_analysis_progress(contract_id: str) -> dict | None:
    import json

    key = f"{ANALYSIS_PREFIX}{contract_id}"
    raw = await redis_client.get(key)
    return json.loads(raw) if raw else None
