from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.blog import Blog


class BlogRepository:

    async def list_all(
        self,
        db: AsyncSession,
    ):
        try:
            result = await db.execute(
            select(Blog)
            .where(Blog.is_active.is_(True))
            .order_by(Blog.created_date.desc())
            )

            return result.scalars().all()
        except Exception as e:
            print("REPO ERROR:", e)
            raise
    
     
    async def get_by_slug(
        self,
        db: AsyncSession,
        slug: str,
    ):
        result = await db.execute(
            select(Blog).where(
                Blog.slug == slug,
                Blog.is_active.is_(True),
            )
        )

        return result.scalars().first()

    async def get_by_id(
        self,
        db: AsyncSession,
        blog_id: int,
    ):
        result = await db.execute(
            select(Blog).where(
                Blog.id == blog_id
            )
        )

        return result.scalars().first()