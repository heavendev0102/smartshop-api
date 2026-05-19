from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.seed_data import DEFAULT_SECTIONS
from app.models.section import Section


class SectionRepository:
    async def get_all(self, db: AsyncSession, active_only: bool = True):
        query = select(Section).order_by(Section.display_order)
        if active_only:
            query = query.where(Section.is_active.is_(True))
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_slug(self, db: AsyncSession, slug: str):
        result = await db.execute(select(Section).where(Section.slug == slug))
        return result.scalars().first()

    async def get_by_slugs(self, db: AsyncSession, slugs: list[str]):
        result = await db.execute(select(Section).where(Section.slug.in_(slugs)))
        return result.scalars().all()

    async def seed_defaults(self, db: AsyncSession):
        created = []
        for item in DEFAULT_SECTIONS:
            existing = await self.get_by_slug(db, item["slug"])
            if existing:
                continue
            section = Section(**item)
            db.add(section)
            created.append(section)
        if created:
            await db.commit()
            for section in created:
                await db.refresh(section)
        return created
