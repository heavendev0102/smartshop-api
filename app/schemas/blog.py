from datetime import datetime

from pydantic import BaseModel


class BlogResponse(BaseModel):
    id: int
    title: str
    slug: str
    image_url: str | None = None
    short_description: str | None = None
    author: str | None = None
    created_date: datetime

    class Config:
        from_attributes = True


class BlogDetailsResponse(BaseModel):
    id: int
    title: str
    slug: str
    image_url: str | None = None
    short_description: str | None = None
    content: str | None = None
    author: str | None = None
    created_date: datetime

    class Config:
        from_attributes = True