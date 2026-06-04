from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), nullable=False)  # NEW
    title = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(500), nullable=False)

    created_date = Column(DateTime(timezone=True), server_default=func.now())
    modified_date = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )