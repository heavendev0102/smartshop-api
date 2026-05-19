from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.seed_data import DEFAULT_CATEGORIES
from app.models.category import Category


class CategoryRepository:
    async def get_all(self, db: AsyncSession, active_only: bool = True):
        query = select(Category).order_by(Category.display_order)
        if active_only:
            query = query.where(Category.is_active.is_(True))
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_slug(self, db: AsyncSession, slug: str):
        result = await db.execute(select(Category).where(Category.slug == slug))
        return result.scalars().first()

    async def get_by_slugs(self, db: AsyncSession, slugs: list[str]):
        result = await db.execute(select(Category).where(Category.slug.in_(slugs)))
        return result.scalars().all()

    async def seed_defaults(self, db: AsyncSession):
        created = []
        for item in DEFAULT_CATEGORIES:
            existing = await self.get_by_slug(db, item["slug"])
            if existing:
                continue
            category = Category(**item)
            db.add(category)
            created.append(category)
        if created:
            await db.commit()
            for category in created:
                await db.refresh(category)
        return created
