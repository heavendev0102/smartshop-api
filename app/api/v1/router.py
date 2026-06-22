from fastapi import APIRouter
from app.api.v1.endpoints import users, products, storefront, wishlist, cart , addresses , delivery_option , orders , blogs

api_router = APIRouter()

api_router.include_router(storefront.router, prefix="/storefront", tags=["Storefront"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(wishlist.router, prefix="/wishlist", tags=["Wishlist"])
api_router.include_router(cart.router, prefix="/cart", tags=["Cart"])
api_router.include_router(addresses.router, prefix="/addresses", tags=["Addresses"])
api_router.include_router(delivery_option.router, prefix="/delivery-options", tags=["Delivery Options"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])
api_router.include_router(orders.router, prefix="/orders",tags=["Orders"])
api_router.include_router(blogs.router,prefix="/blogs",tags=["Blogs"],)