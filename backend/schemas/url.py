from pydantic import BaseModel, HttpUrl

class CreateURLRequest(BaseModel):
    long_url: HttpUrl
    custom_code: str | None = None


class URLResponse(BaseModel):
    short_code: str
    long_url: str