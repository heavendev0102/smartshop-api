from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
)

from app.db.base import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(
        String(255),
        nullable=False,
    )

    slug = Column(
        String(255),
        unique=True,
        nullable=False,
    )

    image_url = Column(String)

    short_description = Column(
        String(500)
    )

    content = Column(Text)

    author = Column(
        String(100)
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    created_date = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )