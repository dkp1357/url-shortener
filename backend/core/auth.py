from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt

from core.security import SECRET_KEY, ALGORITHM

http_bearer = HTTPBearer()

# returns the email of the current user based on the JWT token provided in the Authorization header
def get_current_user(credentials = Depends(http_bearer)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]

    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")