from sqlalchemy import select

from app.models.delivery_option import DeliveryOption


async def get_all_delivery_options(db):
    result = await db.execute(
        select(DeliveryOption)
        .order_by(DeliveryOption.id)
    )

    return result.scalars().all()


class DeliveryOptionRepository:

    async def get_by_id(
        self,
        db,
        delivery_option_id: int,
    ):
        result = await db.execute(
            select(DeliveryOption).where(
                DeliveryOption.id == delivery_option_id
            )
        )

        return result.scalars().first()

    async def get_all(self, db):
        result = await db.execute(
            select(DeliveryOption)
            .order_by(DeliveryOption.id)
        )

        return result.scalars().all()