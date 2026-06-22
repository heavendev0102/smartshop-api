from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.order_item import OrderItem
from app.models.product import Product


class OrderItemRepository:

    async def list_by_order(
        self,
        db,
        order_id: int,
    ):
        result = await db.execute(
            select(OrderItem)
            .options(
                selectinload(OrderItem.product)
            )
            .where(OrderItem.order_id == order_id)
        )

        return result.scalars().all()