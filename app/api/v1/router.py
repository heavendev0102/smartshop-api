from fastapi import APIRouter
from app.api.v1.endpoints import users, products, storefront, wishlist, cart

api_router = APIRouter()

api_router.include_router(storefront.router, prefix="/storefront", tags=["Storefront"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(wishlist.router, prefix="/wishlist", tags=["Wishlist"])
api_router.include_router(cart.router, prefix="/cart", tags=["Cart"])