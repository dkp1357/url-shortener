from db.session import SessionLocal
from core.auth import get_current_user
from core.config import settings

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()