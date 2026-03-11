import redis.asyncio
from .config import settings

redis_client = redis.asyncio.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
)

