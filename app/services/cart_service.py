from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.cart_repo import CartRepository
from app.repositories.product_repo import ProductRepository
from app.schemas.cart import CartItemResponse, CartProductSummary, CartResponse

cart_repo = CartRepository()
product_repo = ProductRepository()


class CartService:
    def _dt(self, value: datetime | None) -> datetime:
        return value or datetime.now(timezone.utc)

    def _to_item_response(self, item) -> CartItemResponse:
        product = item.product
        line_total = Decimal(str(product.current_price)) * item.quantity
        return CartItemResponse(
            id=item.id,
            product_id=item.product_id,
            quantity=item.quantity,
            product=CartProductSummary(
                id=product.id,
                name=product.name,
                image_url=product.image_url,
                current_price=product.current_price,
                stock=product.stock if product.stock is not None else 0,
            ),
            line_total=line_total,
            created_date=self._dt(item.created_date),
            modified_date=self._dt(item.modified_date),
        )

    async def get_cart(self, db: AsyncSession, user_id: int) -> CartResponse:
        items = await cart_repo.list_by_user(db, user_id)
        responses = [self._to_item_response(item) for item in items]
        subtotal = sum((item.line_total for item in responses), Decimal("0.00"))
        item_count = sum(item.quantity for item in responses)
        return CartResponse(items=responses, item_count=item_count, subtotal=subtotal)

    async def add_item(self, db: AsyncSession, user_id: int, product_id: int, quantity: int) -> CartItemResponse:
        product = await product_repo.get_by_id(db, product_id)
        if not product or not product.is_active:
            raise ValueError("Product not found")

        stock = product.stock if product.stock is not None else 0
        existing = await cart_repo.get_by_user_and_product(db, user_id, product_id)
        if existing:
            new_quantity = existing.quantity + quantity
            if new_quantity > stock:
                raise ValueError("Insufficient stock")
            item = await cart_repo.update_quantity(db, existing, new_quantity)
            return self._to_item_response(item)

        if quantity > stock:
            raise ValueError("Insufficient stock")

        item = await cart_repo.create(db, user_id, product_id, quantity)
        return self._to_item_response(item)

    async def update_item(self, db: AsyncSession, user_id: int, item_id: int, quantity: int) -> CartItemResponse:
        item = await cart_repo.get_by_id_for_user(db, item_id, user_id)
        if not item:
            raise ValueError("Cart item not found")

        stock = item.product.stock if item.product.stock is not None else 0
        if quantity > stock:
            raise ValueError("Insufficient stock")

        item = await cart_repo.update_quantity(db, item, quantity)
        return self._to_item_response(item)

    async def remove_item(self, db: AsyncSession, user_id: int, item_id: int) -> None:
        item = await cart_repo.get_by_id_for_user(db, item_id, user_id)
        if not item:
            raise ValueError("Cart item not found")
        await cart_repo.delete(db, item)

    async def clear(self, db: AsyncSession, user_id: int) -> None:
        await cart_repo.clear_for_user(db, user_id)
