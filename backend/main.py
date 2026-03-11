from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from db.session import engine, Base
import models.models

from middleware.rate_limit import RateLimitMiddleware

from api.endpoints.auth import router as auth_router
from api.endpoints.redirect import router as redirect_router
from api.endpoints.url import router as url_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(RateLimitMiddleware)

app.include_router(auth_router)
app.include_router(redirect_router)
app.include_router(url_router)

@app.get("/health", status_code=status.HTTP_200_OK)
async def check_health():
    return {"status": "healthy"}


