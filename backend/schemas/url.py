from pydantic import BaseModel, HttpUrl, ConfigDict
from datetime import datetime

class CreateURLRequest(BaseModel):
    long_url: HttpUrl
    custom_code: str | None = None


class URLResponse(BaseModel):
    short_code: str
    long_url: str


class URLUpdate(BaseModel):
    long_url: HttpUrl | None = None
    expires_at: datetime | None = None
    is_active: bool | None = None


class TopURLResponse(BaseModel):
    short_code: str
    click_count: int
    model_config = ConfigDict(from_attributes=True)