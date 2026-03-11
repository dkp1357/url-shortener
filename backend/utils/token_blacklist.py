from core.redis import redis_client

BLACKLIST_PREFIX = "blacklist:"

async def blacklist_token(token: str, expires_in: int):
    key = BLACKLIST_PREFIX + token
    await redis_client.set(key, "blacklisted", ex=expires_in)


async def is_token_blacklisted(token: str) -> bool:
    key = BLACKLIST_PREFIX + token
    result = await redis_client.get(key)
    return result is not None