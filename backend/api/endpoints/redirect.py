from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from models.models import URL
from api.deps import get_db
from services.analytics import record_click
from services.url_resolver import get_long_url

router = APIRouter(prefix="/r", tags=["redirect"])

@router.get("/{short_code}")
async def redirect(short_code: str, request: Request, db: Session = Depends(get_db)):
    long_url = await get_long_url(short_code, db)

    url_id = db.query(URL).filter(URL.short_code == short_code).first().id

    if not long_url:
        raise HTTPException(status_code=404, detail="URL not found")

    await record_click(db, url_id, request)

    return RedirectResponse(long_url, status_code=302)


