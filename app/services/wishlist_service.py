from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.product_repo import ProductRepository
from app.repositories.wishlist_repo import WishlistRepository
from app.schemas.wishlist import (
    WishlistCheckResponse,
    WishlistItemResponse,
    WishlistProductSummary,
)

wishlist_repo = WishlistRepository()
product_repo = ProductRepository()


class WishlistService:
    def _to_response(self, item) -> WishlistItemResponse:
        product = item.product
        return WishlistItemResponse(
            id=item.id,
            product_id=item.product_id,
            product=WishlistProductSummary(
                id=product.id,
                name=product.name,
                image_url=product.image_url,
                current_price=product.current_price,
                stock=product.stock if product.stock is not None else 0,
                ratings=product.ratings,
            ),
            created_date=item.created_date or datetime.now(timezone.utc),
        )

    async def add_item(self, db: AsyncSession, user_id: int, product_id: int) -> WishlistItemResponse:
        product = await product_repo.get_by_id(db, product_id)
        if not product or not product.is_active:
            raise ValueError("Product not found")

        existing = await wishlist_repo.get_by_user_and_product(db, user_id, product_id)
        if existing:
            item = await wishlist_repo.get_by_id_for_user(db, existing.id, user_id)
            return self._to_response(item)

        item = await wishlist_repo.create(db, user_id, product_id)
        return self._to_response(item)

    async def list_items(self, db: AsyncSession, user_id: int) -> list[WishlistItemResponse]:
        items = await wishlist_repo.list_by_user(db, user_id)
        return [self._to_response(item) for item in items]

    async def remove_item(self, db: AsyncSession, user_id: int, item_id: int) -> None:
        item = await wishlist_repo.get_by_id_for_user(db, item_id, user_id)
        if not item:
            raise ValueError("Wishlist item not found")
        await wishlist_repo.delete(db, item)

    async def clear(self, db: AsyncSession, user_id: int) -> None:
        await wishlist_repo.clear_for_user(db, user_id)

    async def check_product(self, db: AsyncSession, user_id: int, product_id: int) -> WishlistCheckResponse:
        item = await wishlist_repo.get_by_user_and_product(db, user_id, product_id)
        return WishlistCheckResponse(
            product_id=product_id,
            in_wishlist=item is not None,
            wishlist_item_id=item.id if item else None,
        )
