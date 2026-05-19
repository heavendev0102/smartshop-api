from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.product import StorefrontResponse
from app.services.product_service import ProductService

router = APIRouter()
service = ProductService()


@router.get("/", response_model=StorefrontResponse)
async def get_storefront(db: AsyncSession = Depends(get_db)):
    """All storefront data: browse categories + products for each section tab."""
    return await service.get_storefront_data(db)
