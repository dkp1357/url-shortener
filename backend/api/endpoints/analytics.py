from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from api.deps import get_db
from core.auth import get_current_user
from models.models import URL, ClickEvent, User
from typing import List
from schemas.url import TopURLResponse

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/top", response_model=List[TopURLResponse])
def top_urls(db: Session = Depends(get_db), user_email: str = Depends(get_current_user), limit: int | None = 10):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    results = (
        db.query(URL.short_code, URL.click_count)
        .filter(URL.user_id == user.id)
        .order_by(URL.click_count.desc())
        .limit(limit)
        .all()
    )

    return [{"short_code": r.short_code, "click_count": r.click_count} for r in results] or []


@router.get("/{url_id}")
def get_click_count(url_id: int, db: Session = Depends(get_db)):
    count = db.query(func.count(ClickEvent.id)).filter(
        ClickEvent.url_id == url_id
    ).scalar()
    return {"clicks": count}


@router.get("/{url_id}/countries")
def clicks_by_country(url_id: int, db: Session = Depends(get_db)):
    results = db.query(
        ClickEvent.country_code,
        func.count()
    ).filter(
        ClickEvent.url_id == url_id
    ).group_by(
        ClickEvent.country_code
    ).all()
    return results


@router.get("/{short_code}/devices")
def clicks_by_device(short_code: str, db: Session = Depends(get_db)):
    results = db.query(
        ClickEvent.device_type,
        func.count()
    ).join(URL).filter(
        URL.short_code == short_code
    ).group_by(
        ClickEvent.device_type
    ).all()
    return results


@router.get("/{short_code}/timeline")
def click_timeline(short_code: str, db: Session = Depends(get_db)):
    return (
        db.query(
            func.date(ClickEvent.timestamp),
            func.count()
        )
        .join(URL)
        .filter(URL.short_code == short_code)
        .group_by(func.date(ClickEvent.timestamp))
        .all()
    )