from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.order import (
    OrderCreateRequest,
    OrderCreateResponse,
    OrderDetailsResponse,
    OrderHistoryResponse,
)
from app.core.security import get_current_user
from app.db.session import get_db

from app.models.user import User

from app.schemas.order import (
    OrderPreviewRequest,
    OrderPreviewResponse,
)

from app.services.order_service import OrderService

router = APIRouter()

service = OrderService()


@router.post(
    "/preview",
    response_model=OrderPreviewResponse,
)
async def preview_order(
    body: OrderPreviewRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.preview_order(
            db,
            current_user.id,
            body,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    


@router.post(
    "/",
    response_model=OrderCreateResponse,
)
async def place_order(
    body: OrderCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.place_order(
            db,
            current_user.id,
            body,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    
@router.get(
    "/{order_id}",
    response_model=OrderDetailsResponse,
)
async def get_order_details(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.get_order_details(
            db,
            current_user.id,
            order_id,
        )
    except Exception as e:
        print("ERROR =", repr(e))
        raise

@router.get(
    "/",
    response_model=list[OrderHistoryResponse],
)
async def get_order_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await service.get_order_history(
        db,
        current_user.id,
    )