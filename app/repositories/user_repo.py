from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User

class UserRepository:

    async def create(self, db: AsyncSession, user_data: dict):
        user = User(**user_data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_by_email(self, db: AsyncSession, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()