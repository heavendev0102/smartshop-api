from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
)

from app.db.base import Base
from sqlalchemy.orm import relationship

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
    )
    product = relationship("Product")
    quantity = Column(Integer)

    unit_price = Column(Numeric(10, 2))

    line_total = Column(Numeric(10, 2))