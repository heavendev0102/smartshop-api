from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    username = Column(String(100), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    phone_number = Column(String(20))
    gender = Column(String(10))
    date_of_birth = Column(DateTime)
    profile_image = Column(String, nullable=True)
    password_hash = Column(String)
    email_confirmed = Column(Boolean, default=False)
    phone_number_confirmed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    modified_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))