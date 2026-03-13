from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from core.auth import get_current_user
from schemas.url import CreateURLRequest, URLResponse, URLUpdate
from services.url_service import create_url
from core.redis import redis_client
from models.models import URL, User

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



@router.get("/")
def list_urls(user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = db.query(User).filter(User.email == user_email).first().id
    return  db.query(URL).filter(URL.user_id == user_id).all()


@router.get("/{short_code}", response_model=URLResponse, status_code=status.HTTP_200_OK)
def get_single_url(short_code: str, user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = db.query(User).filter(User.email == user_email).first().id
    url = db.query(URL).filter(
        URL.short_code == short_code,
        URL.user_id == user_id
    ).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url


@router.put("/{short_code}", response_model=URLResponse, status_code=status.HTTP_200_OK)
def update_url(short_code: str, payload: URLUpdate, user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = db.query(User).filter(User.email == user_email).first().id

    url = db.query(URL).filter(
        URL.short_code == short_code,
        URL.user_id == user_id
    ).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    if payload.long_url:
        url.long_url = str(payload.long_url)
    if payload.expires_at:
        url.expires_at = payload.expires_at
    if payload.is_active is not None:
        url.is_active = payload.is_active

    db.commit()
    return URLResponse(short_code=url.short_code, long_url=url.long_url)


@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def delete_url(short_code: str, user_email: str = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = db.query(User).filter(User.email == user_email).first().id
    url = db.query(URL).filter(
        URL.short_code == short_code,
        URL.user_id == user_id
    ).first()

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url.is_active = False

    db.commit()

    return {"status": "deleted"}