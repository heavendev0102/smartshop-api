from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.product import (
    ProductCategoryAssign,
    ProductCreate,
    ProductResponse,
    ProductSectionAssign,
    ProductUpdate,
)
from app.services.product_service import ProductService

router = APIRouter()
service = ProductService()


@router.get("/category/{category_slug}", response_model=list[ProductResponse])
async def list_by_category(category_slug: str, db: AsyncSession = Depends(get_db)):
    try:
        return await service.list_by_category(db, category_slug)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await service.create_product(db, product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await service.update_product(db, product_id, product)
    except ValueError as e:
        raise HTTPException(status_code=404 if "not found" in str(e).lower() else 400, detail=str(e))


@router.post("/{product_id}/categories", response_model=ProductResponse)
async def assign_product_categories(
    product_id: int,
    body: ProductCategoryAssign,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await service.assign_categories(db, product_id, body.category_slugs)
    except ValueError as e:
        raise HTTPException(status_code=404 if "not found" in str(e).lower() else 400, detail=str(e))


@router.post("/{product_id}/sections", response_model=ProductResponse)
async def assign_product_sections(
    product_id: int,
    body: ProductSectionAssign,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await service.assign_sections(db, product_id, body.section_slugs)
    except ValueError as e:
        raise HTTPException(status_code=404 if "not found" in str(e).lower() else 400, detail=str(e))
