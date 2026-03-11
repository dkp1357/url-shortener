from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from api.deps import get_db
from models.models import ClickEvent

router = APIRouter(prefix="/analytics", tags=["analytics"])

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