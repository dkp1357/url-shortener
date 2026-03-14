import hashlib
from datetime import datetime, timezone
from services.device_parser import parse_device
from services.geoip import get_country_iso_code
from fastapi.encoders import jsonable_encoder


def hash_ip(ip):
    return hashlib.sha256(ip.encode()).hexdigest()


async def record_click(url_id, request) -> dict:
    ip = request.client.host
    ref = request.headers.get("referer") or "direct" # `referer` because of historical typo in HTTP spec
    ua = request.headers.get("user-agent")

    click_data = jsonable_encoder({
        "url_id": url_id,
        "timestamp": datetime.now(timezone.utc),
        "ip_hash": hash_ip(ip),
        "referrer_host": ref,
        "country_code": get_country_iso_code(ip),
        **parse_device(ua)
    })

    return click_data
