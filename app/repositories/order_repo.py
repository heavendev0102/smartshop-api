from sqlalchemy import select
from app.models.order import Order
from app.models.order_item import OrderItem


class OrderRepository:

    async def create_order(
        self, db, order_data: dict,):
        order = Order(**order_data)
        db.add(order)
        await db.flush()
        await db.refresh(order)
        return order

    async def create_order_item(
        self,
        db,
        order_id: int,
        product_id: int,
        quantity: int,
        unit_price,
        line_total,
    ):
        item = OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price,
            line_total=line_total,
        )

        db.add(item)

        return item

    async def commit(self, db):
        await db.commit()


    from sqlalchemy import select


    async def get_by_id_for_user(
    self,
    db,
    order_id: int,
    user_id: int,
):
        result = await db.execute(
        select(Order).where(
            Order.id == order_id,
            Order.user_id == user_id,
        )
    )

        return result.scalars().first()
    

    async def list_by_user(
        self,
        db,
        user_id: int,
    ):
        result = await db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_date.desc())
        )

        return result.scalars().all()