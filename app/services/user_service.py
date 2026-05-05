from app.repositories.user_repo import UserRepository
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate

repo = UserRepository()

class UserService:

    async def create_user(self, db, user: UserCreate):
        existing = await repo.get_by_email(db, user.email)
        if existing:
            raise Exception("Email already registered")

        user_dict = user.dict()
        password = user_dict.pop("password")

        user_dict["password_hash"] = get_password_hash(password)

        return await repo.create(db, user_dict)

    async def authenticate_user(self, db, email: str, password: str):
        user = await repo.get_by_email(db, email)
        if not user:
            return False
        if not verify_password(password, user.password_hash):
            return False
        return user