import geoip2.database
from core.config import settings

reader = geoip2.database.Reader(settings.GEOIP2_DB_PATH)

def get_country_iso_code(ip: str):
    try:
        response = reader.country(ip)
        return response.country.iso_code
    except Exception:
        raise Exception("Invalid IP address or GeoIP lookup failed")