from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timezone

from core.redis import redis_client
from models.models import URL

CACHE_PREFIX = "url:"

async def get_long_url(short_code, db: Session):
    cache_key = CACHE_PREFIX + short_code
    cached = await redis_client.get(cache_key)

    if cached:
        return cached

    url = db.query(URL).filter(URL.short_code == short_code, URL.is_active, or_(
            URL.expires_at == None,
            URL.expires_at > datetime.now(timezone.utc)
        )
    ).first()

    if not url:
        return None

    await redis_client.set(cache_key, url.long_url, ex=3600)
    return url.long_url