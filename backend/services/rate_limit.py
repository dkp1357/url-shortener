import time
from core.redis import redis_client
from core.config import settings

RATE_LIMIT = settings.RATE_LIMIT
WINDOW = settings.RATE_LIMIT_WINDOW

async def is_rate_limited(ip: str):
    key = f"rate:{ip}"
    now = int(time.time())
    window_start = now - WINDOW
    await redis_client.zremrangebyscore(key, 0, window_start)
    await redis_client.zadd(key, {now: now})
    count = await redis_client.zcard(key)
    await redis_client.expire(key, WINDOW)
    return count > RATE_LIMIT