from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse
from app.services.user_service import UserService
from app.core.security import create_access_token, get_current_user
from app.db.session import get_db
from app.models.user import User

router = APIRouter()
service = UserService()

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await service.create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    authenticated_user = await service.authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create JWT token
    access_token = create_access_token(data={"sub": str(authenticated_user.id), "email": authenticated_user.email})

    # Convert user to dict for response
    user_data = {
        "id": authenticated_user.id,
        "first_name": authenticated_user.first_name,
        "last_name": authenticated_user.last_name,
        "username": authenticated_user.username,
        "email": authenticated_user.email,
        "is_active": authenticated_user.is_active,
        "created_date": authenticated_user.created_date,
        "modified_date": authenticated_user.modified_date,
    }

    return TokenResponse(access_token=access_token, user=user_data)

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user