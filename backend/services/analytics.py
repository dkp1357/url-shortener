import hashlib
from models.models import ClickEvent
from datetime import datetime, timezone


def hash_ip(ip):
    return hashlib.sha256(ip.encode()).hexdigest()


async def record_click(db, url_id, request):
    ip = request.client.host
    # `referer` because of historical typo in HTTP spec
    referrer = request.headers.get("referer") or "direct"

    click = ClickEvent(
        url_id=url_id,
        timestamp=datetime.now(timezone.utc),
        ip_hash=hash_ip(ip),
        referrer_host=referrer
    )

    db.add(click)
    db.commit()