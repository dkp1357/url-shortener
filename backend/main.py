from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from db.session import engine, Base
import models.models

from middleware.rate_limit import RateLimitMiddleware

from api.endpoints.auth import router as auth_router
from api.endpoints.redirect import router as redirect_router
from api.endpoints.url import router as url_router
from api.endpoints.analytics import router as analytics_router

from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
import services.rabbitmq as rabbitmq_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    await rabbitmq_service.connect_rabbitmq()
    yield
    await rabbitmq_service.close_rabbitmq()


origins = settings.ALLOWED_ORIGINS.split(",")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware)

app.include_router(auth_router)
app.include_router(redirect_router)
app.include_router(url_router)
app.include_router(analytics_router)


@app.get("/health", status_code=status.HTTP_200_OK)
async def check_health():
    return {"status": "healthy"}
