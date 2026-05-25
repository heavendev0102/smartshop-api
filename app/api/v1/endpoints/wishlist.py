from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.wishlist import WishlistCheckResponse, WishlistItemCreate, WishlistItemResponse
from app.services.wishlist_service import WishlistService

router = APIRouter()
service = WishlistService()


@router.post("/items", response_model=WishlistItemResponse, status_code=201)
async def add_wishlist_item(
    body: WishlistItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await service.add_item(db, current_user.id, body.product_id)
    except ValueError as e:
        raise HTTPException(status_code=404 if "not found" in str(e).lower() else 400, detail=str(e))


@router.get("/", response_model=list[WishlistItemResponse])
async def get_wishlist(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await service.list_items(db, current_user.id)


@router.delete("/items/{wishlist_item_id}", status_code=204)
async def remove_wishlist_item(
    wishlist_item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        await service.remove_item(db, current_user.id, wishlist_item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/", status_code=204)
async def clear_wishlist(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await service.clear(db, current_user.id)


@router.get("/check/{product_id}", response_model=WishlistCheckResponse)
async def check_wishlist_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await service.check_product(db, current_user.id, product_id)
