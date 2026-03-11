from sqlalchemy import select
from models.models import User

async def get_user_id_by_email(db, email):
    result = await db.execute(
        select(User.id).where(User.email == email)
    )
    return result.scalar_one_or_none()