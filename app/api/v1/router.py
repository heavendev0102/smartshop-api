from fastapi import APIRouter
from app.api.v1.endpoints import users, products, storefront

api_router = APIRouter()

api_router.include_router(storefront.router, prefix="/storefront", tags=["Storefront"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])