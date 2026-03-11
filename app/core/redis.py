import redis.asyncio as redis

from app.core.config import get_settings

settings = get_settings()


async def get_redis() -> redis.Redis:
    return redis.from_url(settings.redis_url, decode_responses=True)
