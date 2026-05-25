from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_review import ProductReview


class ReviewRepository:
    async def get_by_product_id(self, db: AsyncSession, product_id: int):
        query = (
            select(ProductReview)
            .where(ProductReview.product_id == product_id)
            .order_by(ProductReview.created_date.desc())
        )
        result = await db.execute(query)
        return result.scalars().all()

    async def get_rating_summary(self, db: AsyncSession, product_id: int):
        counts_query = (
            select(ProductReview.rating, func.count())
            .where(ProductReview.product_id == product_id)
            .group_by(ProductReview.rating)
        )
        result = await db.execute(counts_query)
        rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        total = 0
        weighted_sum = 0
        for rating, count in result.all():
            rating_counts[int(rating)] = int(count)
            total += int(count)
            weighted_sum += int(rating) * int(count)

        average = round(weighted_sum / total, 2) if total > 0 else None
        return average, total, rating_counts
