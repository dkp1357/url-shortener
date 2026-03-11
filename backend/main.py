from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from db.session import engine, Base
import models.models


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/health", status_code=status.HTTP_200_OK)
async def check_health():
    return {"status": "healthy"}


