from fastapi import HTTPException

from models.models import URL
from utils.base62 import encode
import secrets
import string

def create_short_code(db, long_url, user_id):
    url = URL(
        long_url=long_url,
        user_id=user_id
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    short_code = encode(url.id)

    url.short_code = short_code

    db.commit()
    db.refresh(url)

    return url


def generate_random_code(length: int = 7):
    return "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))


def generate_unique_code(db, length=7):
    while True:
        code = generate_random_code(length)
        exists = db.query(URL).filter(URL.short_code == code).first()
        if not exists:
            return code


def create_custom_code(db, long_url, user_id, custom_code):
    exists = db.query(URL).filter(URL.short_code == custom_code).first()

    if exists:
        raise HTTPException(status_code=409, detail="short code already taken")

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