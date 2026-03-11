from pydantic import HttpUrl
from sqlalchemy.orm import Session
from models.models import URL
import utils.shortener as shortener

from sqlalchemy import or_
from datetime import datetime, timezone

from fastapi import HTTPException


def create_url(db: Session, long_url: HttpUrl, user_id: int, custom_code: str | None):
    long_url = str(long_url)
    if custom_code:
        exists = db.query(URL).filter(URL.short_code == custom_code, URL.is_active, or_(
            URL.expires_at == None,
            URL.expires_at > datetime.now(timezone.utc)
        )).first()

        if exists:
            raise HTTPException(status_code=409, detail="code already taken")

        url = URL(
            long_url=long_url,
            short_code=custom_code,
            user_id=user_id,
            is_custom=True
        )

        db.add(url)
        db.commit()
        db.refresh(url)
        return url

    short_code = shortener.generate_unique_code(db, length=7)

    url = URL(
        long_url=long_url,
        short_code=short_code,
        user_id=user_id
    )

    db.add(url)
    db.commit()
    db.refresh(url)
    return url
