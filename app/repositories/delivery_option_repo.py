from sqlalchemy import select

from app.models.delivery_option import DeliveryOption


async def get_all_delivery_options(db):
    result = await db.execute(
        select(DeliveryOption)
        .order_by(DeliveryOption.id)
    )

    return result.scalars().all()