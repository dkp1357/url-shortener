from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timezone

from core.redis import redis_client
from models.models import URL

CACHE_PREFIX = "url:"

async def get_cached_url(code: str):
    return await redis_client.get(CACHE_PREFIX + code)


async def cache_url(code: str, url: str):
    await redis_client.set(
        CACHE_PREFIX + code,
        url,
        ex=3600
    )

async def get_long_url(short_code, db: Session):
    cached = await get_cached_url(short_code)

    if cached:
        return cached

    url = db.query(URL).filter(URL.short_code == short_code, URL.is_active, or_(
            URL.expires_at == None,
            URL.expires_at > datetime.now(timezone.utc)
        )
    ).first()

    if not url:
        return None

    await cache_url(short_code, url.long_url)
    return url.long_url