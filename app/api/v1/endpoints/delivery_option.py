from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.delivery_option import (
    DeliveryOptionResponse,
)
from app.services.delivery_option_service import (
    fetch_delivery_options,
)

router = APIRouter()


@router.get(
    "/delivery-options",
    response_model=list[DeliveryOptionResponse]
)
async def get_delivery_options(
    db: AsyncSession = Depends(get_db),
):
    try:
        return await fetch_delivery_options(db)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        print(f"Delivery Options Error: {e}")

        raise HTTPException(
            status_code=500,
            detail=str(e)  # For debugging only
        )


