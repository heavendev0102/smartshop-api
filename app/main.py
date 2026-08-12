from contextlib import asynccontextmanager


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.migrate import run_migrations
from app.db.seed import seed_database
from app.db.session import AsyncSessionLocal


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     run_migrations()
#     async with AsyncSessionLocal() as db:
#         await seed_database(db)
#     yield


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("1. Starting lifespan")

    print("2. Before migrations")
    run_migrations()
    print("3. After migrations")

    print("4. Before DB session")
    async with AsyncSessionLocal() as db:
        print("5. DB session opened")

        print("6. Before seed")
        await seed_database(db)
        print("7. After seed")

    print("8. Startup complete")
    yield


app = FastAPI(title="Enterprise FastAPI App", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")