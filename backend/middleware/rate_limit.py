from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException

from services.rate_limit import is_rate_limited

EXCLUDED_PATHS = {
    "/health",
    "/docs",
}

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host

        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        if await is_rate_limited(ip):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        response = await call_next(request)
        return response