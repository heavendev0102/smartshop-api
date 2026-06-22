from app.repositories.blog_repo import (
    BlogRepository,
)

repo = BlogRepository()


class BlogService:

    async def get_blogs(
        self,
        db,
    ):
        try:
           return await repo.list_all(db)

        except Exception as e:
            print("SERVICE ERROR:", e)
            raise
        

    async def get_blog_details(
        self,
        db,
        slug: str,
    ):
        blog = await repo.get_by_slug(
            db,
            slug,
        )

        if not blog:
            raise ValueError(
                "Blog not found"
            )

        return blog