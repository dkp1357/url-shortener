from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from core.token_blacklist import is_token_blacklisted
import jwt

from core.security import SECRET_KEY, ALGORITHM

http_bearer = HTTPBearer()

# returns the email of the current user based on the JWT token provided in the Authorization header
async def get_current_user(credentials = Depends(http_bearer)):
    token = credentials.credentials

    if await is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token revoked")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")