from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.wishlist_item import WishlistItem


class WishlistRepository:
    async def get_by_id_for_user(self, db: AsyncSession, item_id: int, user_id: int):
        query = (
            select(WishlistItem)
            .options(selectinload(WishlistItem.product))
            .where(WishlistItem.id == item_id, WishlistItem.user_id == user_id)
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_user_and_product(self, db: AsyncSession, user_id: int, product_id: int):
        query = select(WishlistItem).where(
            WishlistItem.user_id == user_id,
            WishlistItem.product_id == product_id,
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def list_by_user(self, db: AsyncSession, user_id: int):
        query = (
            select(WishlistItem)
            .options(selectinload(WishlistItem.product))
            .where(WishlistItem.user_id == user_id)
            .order_by(WishlistItem.created_date.desc())
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, user_id: int, product_id: int):
        item = WishlistItem(user_id=user_id, product_id=product_id)
        db.add(item)
        await db.commit()
        return await self.get_by_id_for_user(db, item.id, user_id)

    async def delete(self, db: AsyncSession, item: WishlistItem):
        await db.delete(item)
        await db.commit()

    async def clear_for_user(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(WishlistItem).where(WishlistItem.user_id == user_id))
        items = result.scalars().all()
        for item in items:
            await db.delete(item)
        await db.commit()
