from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.blog import (
    BlogDetailsResponse,
)

from app.services.blog_service import (
    BlogService,
)

router = APIRouter()

service = BlogService()


@router.get("/")
async def get_blogs_all(
    db: AsyncSession = Depends(get_db),
):
    try:

        blogs = await service.get_blogs(db)

        return blogs

    except Exception as e:
        print("BLOG ERROR:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


@router.get(
    "/{slug}",
    response_model=BlogDetailsResponse,
)
async def get_blog_details(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await service.get_blog_details(
            db,
            slug,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )