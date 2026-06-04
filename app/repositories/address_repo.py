from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.address import Address


class AddressRepository:
    async def get_by_id(self, db: AsyncSession, address_id: int):
        result = await db.execute(
            select(Address).where(Address.id == address_id)
        )
        return result.scalars().first()

    async def get_by_id_for_user(
        self,
        db: AsyncSession,
        address_id: int,
        user_id: int,
    ):
        result = await db.execute(
            select(Address).where(
                Address.id == address_id,
                Address.user_id == user_id,
            )
        )
        return result.scalars().first()

    async def list_by_user(
        self,
        db: AsyncSession,
        user_id: int,
    ):
        result = await db.execute(
            select(Address)
            .where(Address.user_id == user_id)
            .order_by(Address.created_date.desc())
        )
        return result.scalars().all()

    async def create(
        self,
        db: AsyncSession,
        user_id: int,
        title: str,
        phone: str,
        address: str,
        status: str,
    ):
        item = Address(
            user_id=user_id,
            title=title,
            phone=phone,
            address=address,
            status=status,
        )

        db.add(item)
        await db.commit()
        await db.refresh(item)

        return item

    async def update(
        self,
        db: AsyncSession,
        item: Address,
        title: str,
        phone: str,
        address: str,
        status: str,
    ):
        item.title = title
        item.phone = phone
        item.address = address
        item.status = status
        
        await db.commit()
        await db.refresh(item)
        return item

    async def delete(
        self,
        db: AsyncSession,
        item: Address,
    ):
        await db.delete(item)
        await db.commit()