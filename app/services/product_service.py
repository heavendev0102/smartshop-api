from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.seed import seed_database
from app.db.seed_data import DEFAULT_CATEGORIES, DEFAULT_SECTIONS
from app.repositories.category_repo import CategoryRepository
from app.repositories.product_repo import ProductRepository
from app.repositories.section_repo import SectionRepository
from app.repositories.review_repo import ReviewRepository
from app.schemas.product import (
    CategoryResponse,
    ProductReviewResponse,
    RatingSummaryResponse,
    StorefrontResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    SectionResponse,
    SectionWithProductsResponse,
)

VALID_CATEGORY_SLUGS = {c["slug"] for c in DEFAULT_CATEGORIES}
VALID_SECTION_SLUGS = {s["slug"] for s in DEFAULT_SECTIONS}

category_repo = CategoryRepository()
section_repo = SectionRepository()
product_repo = ProductRepository()
review_repo = ReviewRepository()


class ProductService:
    @staticmethod
    def _dt(value: datetime | None) -> datetime:
        return value or datetime.now(timezone.utc)

    def _to_response(self, product) -> ProductResponse:
        categories = [
            CategoryResponse.model_validate(pc.category)
            for pc in product.product_categories
            if pc.category
        ]
        sections = [
            SectionResponse.model_validate(ps.section)
            for ps in product.product_sections
            if ps.section
        ]
        return ProductResponse(
            id=product.id,
            name=product.name,
            image_url=product.image_url,
            description=product.description,
            stock=product.stock if product.stock is not None else 0,
            ratings=product.ratings,
            current_price=product.current_price,
            original_price=product.original_price,
            discount_percent=product.discount_percent,
            is_active=bool(product.is_active),
            categories=categories,
            sections=sections,
            created_date=self._dt(product.created_date),
            modified_date=self._dt(product.modified_date),
        )

    async def _resolve_category_ids(self, db: AsyncSession, slugs: list[str]) -> list[int]:
        if not slugs:
            raise ValueError("At least one category slug is required")
        invalid = set(slugs) - VALID_CATEGORY_SLUGS
        if invalid:
            raise ValueError(f"Invalid category slugs: {', '.join(sorted(invalid))}")

        categories = await category_repo.get_by_slugs(db, slugs)
        found_slugs = {c.slug for c in categories}
        missing = set(slugs) - found_slugs
        if missing:
            raise ValueError(f"Categories not found: {', '.join(sorted(missing))}")
        return [c.id for c in categories]

    async def _resolve_section_ids(self, db: AsyncSession, slugs: list[str]) -> list[int]:
        if not slugs:
            return []
        invalid = set(slugs) - VALID_SECTION_SLUGS
        if invalid:
            raise ValueError(f"Invalid section slugs: {', '.join(sorted(invalid))}")

        sections = await section_repo.get_by_slugs(db, slugs)
        found_slugs = {s.slug for s in sections}
        missing = set(slugs) - found_slugs
        if missing:
            raise ValueError(f"Sections not found: {', '.join(sorted(missing))}")
        return [s.id for s in sections]

    def _calc_discount(self, current_price: Decimal, original_price: Decimal | None, discount_percent: int | None):
        if discount_percent is not None:
            return discount_percent
        if original_price and original_price > current_price:
            return int(((original_price - current_price) / original_price) * 100)
        return None

    async def list_by_section(self, db: AsyncSession, slug: str) -> list[ProductResponse]:
        await seed_database(db)
        products = await product_repo.get_by_section_slug(db, slug)
        return [self._to_response(p) for p in products]

    async def list_by_category(self, db: AsyncSession, slug: str) -> list[ProductResponse]:
        await seed_database(db)
        products = await product_repo.get_by_category_slug(db, slug)
        return [self._to_response(p) for p in products]

    async def get_storefront_data(self, db: AsyncSession) -> StorefrontResponse:
        await seed_database(db)

        categories = [
            CategoryResponse.model_validate(c)
            for c in await category_repo.get_all(db)
        ]

        section_meta = {s.slug: s for s in await section_repo.get_all(db)}

        async def section_products(slug: str) -> SectionWithProductsResponse:
            section = section_meta.get(slug)
            products = await product_repo.get_by_section_slug(db, slug)
            return SectionWithProductsResponse(
                name=section.name if section else slug.replace("_", " ").title(),
                slug=slug,
                products=[self._to_response(p) for p in products],
            )

        return StorefrontResponse(
            categories=categories,
            new_arrivals=await section_products("new_arrivals"),
            bestsellers=await section_products("bestsellers"),
            featured=await section_products("featured"),
        )

    async def get_product(self, db: AsyncSession, product_id: int) -> ProductResponse | None:
        product = await product_repo.get_by_id(db, product_id)
        if not product:
            return None
        return self._to_response(product)

    async def create_product(self, db: AsyncSession, data: ProductCreate) -> ProductResponse:
        category_ids = await self._resolve_category_ids(db, data.category_slugs)
        section_ids = await self._resolve_section_ids(db, data.section_slugs)
        payload = data.model_dump(exclude={"category_slugs", "section_slugs"})
        payload["discount_percent"] = self._calc_discount(
            data.current_price, data.original_price, data.discount_percent
        )
        product = await product_repo.create(db, payload, category_ids, section_ids)
        return self._to_response(product)

    async def update_product(self, db: AsyncSession, product_id: int, data: ProductUpdate) -> ProductResponse:
        product = await product_repo.get_by_id(db, product_id)
        if not product:
            raise ValueError("Product not found")

        update_data = data.model_dump(exclude_unset=True, exclude={"category_slugs", "section_slugs"})
        if "current_price" in update_data or "original_price" in update_data:
            current = update_data.get("current_price", product.current_price)
            original = update_data.get("original_price", product.original_price)
            discount = update_data.get("discount_percent", product.discount_percent)
            update_data["discount_percent"] = self._calc_discount(current, original, discount)

        if update_data:
            product = await product_repo.update(db, product, update_data)

        if data.category_slugs is not None:
            category_ids = await self._resolve_category_ids(db, data.category_slugs)
            product = await product_repo.set_categories(db, product, category_ids)

        if data.section_slugs is not None:
            section_ids = await self._resolve_section_ids(db, data.section_slugs)
            product = await product_repo.set_sections(db, product, section_ids)

        return self._to_response(product)

    async def assign_categories(self, db: AsyncSession, product_id: int, slugs: list[str]) -> ProductResponse:
        product = await product_repo.get_by_id(db, product_id)
        if not product:
            raise ValueError("Product not found")
        category_ids = await self._resolve_category_ids(db, slugs)
        product = await product_repo.set_categories(db, product, category_ids)
        return self._to_response(product)

    async def assign_sections(self, db: AsyncSession, product_id: int, slugs: list[str]) -> ProductResponse:
        product = await product_repo.get_by_id(db, product_id)
        if not product:
            raise ValueError("Product not found")
        section_ids = await self._resolve_section_ids(db, slugs)
        product = await product_repo.set_sections(db, product, section_ids)
        return self._to_response(product)

    async def get_recommended(self, db: AsyncSession, product_id: int) -> list[ProductResponse]:
        await seed_database(db)
        product, recommended = await product_repo.get_recommended(db, product_id)
        if not product:
            raise ValueError("Product not found")
        return [self._to_response(p) for p in recommended]

    async def get_reviews(self, db: AsyncSession, product_id: int) -> list[ProductReviewResponse]:
        product = await product_repo.get_by_id(db, product_id)
        if not product:
            raise ValueError("Product not found")
        reviews = await review_repo.get_by_product_id(db, product_id)
        return [ProductReviewResponse.model_validate(r) for r in reviews]

    async def get_rating_summary(self, db: AsyncSession, product_id: int) -> RatingSummaryResponse:
        product = await product_repo.get_by_id(db, product_id)
        if not product:
            raise ValueError("Product not found")
        average, total, rating_counts = await review_repo.get_rating_summary(db, product_id)
        if average is not None:
            await product_repo.update_ratings(db, product_id, average)
        return RatingSummaryResponse(
            average_rating=average,
            total_reviews=total,
            rating_counts=rating_counts,
        )
    
    async def search_products(
    self,
    db: AsyncSession,
    q: str,
    ) -> list[ProductResponse]:

        products = await product_repo.search_products(db, q)

        return [self._to_response(product) for product in products]
