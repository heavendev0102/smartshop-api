from operator import or_
from unittest import result

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.category import Category
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.product_section import ProductSection
from app.models.section import Section


class ProductRepository:
    async def _product_query(self):
        return select(Product).options(
            selectinload(Product.product_categories).selectinload(ProductCategory.category),
            selectinload(Product.product_sections).selectinload(ProductSection.section),
        )

    async def get_by_id(self, db: AsyncSession, product_id: int):
        query = (await self._product_query()).where(Product.id == product_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_by_category_slug(self, db: AsyncSession, slug: str):
        query = (
            (await self._product_query())
            .join(Product.product_categories)
            .join(ProductCategory.category)
            .where(
                Category.slug == slug,
                Product.is_active.is_(True),
                Category.is_active.is_(True),
            )
            .order_by(Product.created_date.desc())
        )
        result = await db.execute(query)
        return result.scalars().unique().all()

    async def get_by_section_slug(self, db: AsyncSession, slug: str):
        query = (
            (await self._product_query())
            .join(Product.product_sections)
            .join(ProductSection.section)
            .where(
                Section.slug == slug,
                Product.is_active.is_(True),
                Section.is_active.is_(True),
            )
            .order_by(Product.created_date.desc())
        )
        result = await db.execute(query)
        return result.scalars().unique().all()

    async def create(
        self,
        db: AsyncSession,
        product_data: dict,
        category_ids: list[int],
        section_ids: list[int] | None = None,
    ):
        product = Product(**product_data)
        db.add(product)
        await db.flush()
        for category_id in category_ids:
            db.add(ProductCategory(product_id=product.id, category_id=category_id))
        for section_id in section_ids or []:
            db.add(ProductSection(product_id=product.id, section_id=section_id))
        await db.commit()
        return await self.get_by_id(db, product.id)

    async def update(self, db: AsyncSession, product: Product, product_data: dict):
        for key, value in product_data.items():
            setattr(product, key, value)
        await db.commit()
        return await self.get_by_id(db, product.id)

    async def set_categories(self, db: AsyncSession, product: Product, category_ids: list[int]):
        product.product_categories.clear()
        await db.flush()
        for category_id in category_ids:
            db.add(ProductCategory(product_id=product.id, category_id=category_id))
        await db.commit()
        return await self.get_by_id(db, product.id)

    async def set_sections(self, db: AsyncSession, product: Product, section_ids: list[int]):
        product.product_sections.clear()
        await db.flush()
        for section_id in section_ids:
            db.add(ProductSection(product_id=product.id, section_id=section_id))
        await db.commit()
        return await self.get_by_id(db, product.id)

    async def get_recommended(self, db: AsyncSession, product_id: int, limit: int = 10):
        product = await self.get_by_id(db, product_id)
        if not product:
            return None, []

        category_ids = [pc.category_id for pc in product.product_categories if pc.category_id]
        if not category_ids:
            query = (
                (await self._product_query())
                .where(Product.id != product_id, Product.is_active.is_(True))
                .order_by(Product.ratings.desc().nullslast(), Product.created_date.desc())
                .limit(limit)
            )
        else:
            query = (
                (await self._product_query())
                .join(Product.product_categories)
                .where(
                    ProductCategory.category_id.in_(category_ids),
                    Product.id != product_id,
                    Product.is_active.is_(True),
                )
                .order_by(Product.ratings.desc().nullslast(), Product.created_date.desc())
                .limit(limit)
            )
        result = await db.execute(query)
        return product, result.scalars().unique().all()

    async def update_ratings(self, db: AsyncSession, product_id: int, average_rating):
        product = await db.get(Product, product_id)
        if product:
            product.ratings = average_rating
            await db.commit()
        return product
    
    async def search_products(self,db: AsyncSession,q: str,):
        query = ((await self._product_query())
        .where(
        or_(
        Product.name.ilike(f"%{q}%"),
        Product.description.ilike(f"%{q}%")
        ),
        Product.is_active.is_(True)
        )
        )

        result = await db.execute(query)
        return result.scalars().unique().all()
