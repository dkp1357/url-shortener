from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from core.auth import get_current_user
from schemas.url import CreateURLRequest, URLResponse
from services.url_service import create_url
from core.redis import redis_client
from models.models import User

router = APIRouter(prefix="/urls", tags=["urls"])

@router.post("/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    request: CreateURLRequest,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    try:
        user_id = db.query(User).filter(User.email == user_email).first().id
        url = create_url(db, request.long_url, user_id, request.custom_code)

        await redis_client.set(
            f"url:{url.short_code}",
            url.long_url,
            ex=3600
        )

        return URLResponse(short_code=url.short_code, long_url=url.long_url)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



