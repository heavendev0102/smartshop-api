from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.repositories.delivery_option_repo import (
    get_all_delivery_options,
)

async def fetch_delivery_options(db):
    options = await get_all_delivery_options(db)

    response = []

    for option in options:

        estimated_date = None

        if option.delivery_days:
            estimated_date = (
                date.today()
                + timedelta(days=option.delivery_days)
            )

        response.append(
            {
                "id": option.id,
                "name": option.name,
                "description": option.description,
                "charge": option.charge,
                "delivery_days": option.delivery_days,
                "estimated_delivery_date": estimated_date,
            }
        )

    return response