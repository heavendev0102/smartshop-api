from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    address_id = Column(
        Integer,
        ForeignKey("addresses.id"),
        nullable=False,
    )

    delivery_option_id = Column(
        Integer,
        ForeignKey("delivery_options.id"),
        nullable=False,
    )

    delivery_date = Column(Date)
    items = relationship(
    "OrderItem",
    cascade="all, delete-orphan",
)
    payment_method = Column(
        String(50),
        nullable=False,
    )

    payment_status = Column(
        String(50),
        default="pending",
    )

    order_status = Column(
        String(50),
        default="placed",
    )

    subtotal = Column(Numeric(10, 2))
    estimated_tax = Column(Numeric(10, 2))
    shipping_charge = Column(Numeric(10, 2))
    total = Column(Numeric(10, 2))

    created_date = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )