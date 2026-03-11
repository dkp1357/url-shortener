from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from api.deps import get_db, get_current_user

from utils.token_blacklist import blacklist_token
from models.models import User
from schemas.dto import RegisterRequest, LoginRequest, TokenResponse
import core.security as security

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == request.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=request.email,
        password_hash=security.hash_password(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "user created"}


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User does not exist, Register first please")

    if not security.verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = security.create_access_token(data={"sub": user.email})

    return TokenResponse(access_token=access_token)


http_bearer = HTTPBearer()

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(credentials = Depends(http_bearer)):
    token = credentials.credentials
    ttl = security.token_expiry_in_seconds(token)
    await blacklist_token(token, ttl)
    return {"message": "logout successful"}


@router.get("/me")
async def me(user_email = Depends(get_current_user)):
    return {"user_email": user_email}