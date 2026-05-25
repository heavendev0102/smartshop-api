from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart_item import CartItem


class CartRepository:
    async def get_by_id_for_user(self, db: AsyncSession, item_id: int, user_id: int):
        query = (
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.id == item_id, CartItem.user_id == user_id)
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_user_and_product(self, db: AsyncSession, user_id: int, product_id: int):
        query = select(CartItem).where(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id,
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def list_by_user(self, db: AsyncSession, user_id: int):
        query = (
            select(CartItem)
            .options(selectinload(CartItem.product))
            .where(CartItem.user_id == user_id)
            .order_by(CartItem.created_date.desc())
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, user_id: int, product_id: int, quantity: int):
        item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
        db.add(item)
        await db.commit()
        return await self.get_by_id_for_user(db, item.id, user_id)

    async def update_quantity(self, db: AsyncSession, item: CartItem, quantity: int):
        item.quantity = quantity
        item.modified_date = datetime.now(timezone.utc)
        await db.commit()
        return await self.get_by_id_for_user(db, item.id, item.user_id)

    async def delete(self, db: AsyncSession, item: CartItem):
        await db.delete(item)
        await db.commit()

    async def clear_for_user(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(CartItem).where(CartItem.user_id == user_id))
        items = result.scalars().all()
        for item in items:
            await db.delete(item)
        await db.commit()
