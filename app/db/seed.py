from datetime import datetime, timezone

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.seed_data import DEFAULT_CATEGORIES, DEFAULT_SECTIONS, DUMMY_PRODUCTS
from app.models.category import Category
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.product_section import ProductSection
from app.models.section import Section
from app.repositories.product_repo import ProductRepository

product_repo = ProductRepository()


async def seed_database(db: AsyncSession) -> None:
    """Seed browse categories, homepage sections, and dummy products."""
    await _seed_categories(db)
    await _seed_sections(db)

    product_count = await db.scalar(select(func.count()).select_from(Product)) or 0
    if product_count == 0:
        await _create_dummy_products(db)
    else:
        await _repair_product_links(db)

    await _backfill_product_fields(db)
    await _backfill_null_timestamps(db)
    await db.commit()


async def _backfill_product_fields(db: AsyncSession) -> None:
    """Backfill description, stock, and ratings on existing seeded products."""
    result = await db.execute(select(Product))
    products_by_name = {p.name: p for p in result.scalars().all()}

    for item in DUMMY_PRODUCTS:
        product = products_by_name.get(item["name"])
        if not product:
            continue
        if product.description is None and item.get("description"):
            product.description = item["description"]
        if product.stock is None or product.stock == 0:
            product.stock = item.get("stock", 0)
        if product.ratings is None and item.get("ratings") is not None:
            product.ratings = item["ratings"]


async def _backfill_null_timestamps(db: AsyncSession) -> None:
    now = datetime.now(timezone.utc)
    await db.execute(
        update(Product).where(Product.created_date.is_(None)).values(created_date=now, modified_date=now)
    )
    await db.execute(
        update(Product).where(Product.modified_date.is_(None)).values(modified_date=now)
    )
    await db.execute(
        update(Category).where(Category.created_date.is_(None)).values(created_date=now, modified_date=now)
    )
    await db.execute(
        update(Section).where(Section.created_date.is_(None)).values(created_date=now, modified_date=now)
    )


async def _seed_categories(db: AsyncSession) -> None:
    result = await db.execute(select(Category))
    existing = {c.slug: c for c in result.scalars().all()}

    for item in DEFAULT_CATEGORIES:
        category = existing.get(item["slug"])
        if not category:
            db.add(Category(**item))
        elif not category.icon_url and item.get("icon_url"):
            category.icon_url = item["icon_url"]


async def _seed_sections(db: AsyncSession) -> None:
    result = await db.execute(select(Section.slug))
    existing_slugs = set(result.scalars().all())

    for item in DEFAULT_SECTIONS:
        if item["slug"] not in existing_slugs:
            db.add(Section(**item))


async def _create_dummy_products(db: AsyncSession) -> None:
    categories = await db.execute(select(Category))
    sections = await db.execute(select(Section))
    category_slug_to_id = {c.slug: c.id for c in categories.scalars().all()}
    section_slug_to_id = {s.slug: s.id for s in sections.scalars().all()}

    for item in DUMMY_PRODUCTS:
        category_ids = [category_slug_to_id[slug] for slug in item["category_slugs"]]
        section_ids = [section_slug_to_id[slug] for slug in item["section_slugs"]]
        product_data = {
            "name": item["name"],
            "image_url": item["image_url"],
            "description": item.get("description"),
            "stock": item.get("stock", 0),
            "ratings": item.get("ratings"),
            "current_price": item["current_price"],
            "original_price": item["original_price"],
            "discount_percent": item["discount_percent"],
            "is_active": True,
        }
        await product_repo.create(db, product_data, category_ids, section_ids)


async def _repair_product_links(db: AsyncSession) -> None:
    """Re-link existing products when sections/categories were migrated but links are missing."""
    result = await db.execute(select(Product))
    products_by_name = {p.name: p for p in result.scalars().all()}

    categories = await db.execute(select(Category))
    sections = await db.execute(select(Section))
    category_slug_to_id = {c.slug: c.id for c in categories.scalars().all()}
    section_slug_to_id = {s.slug: s.id for s in sections.scalars().all()}

    for item in DUMMY_PRODUCTS:
        product = products_by_name.get(item["name"])
        if not product:
            continue

        for slug in item["category_slugs"]:
            category_id = category_slug_to_id.get(slug)
            if not category_id:
                continue
            exists = await db.scalar(
                select(func.count())
                .select_from(ProductCategory)
                .where(
                    ProductCategory.product_id == product.id,
                    ProductCategory.category_id == category_id,
                )
            )
            if not exists:
                db.add(ProductCategory(product_id=product.id, category_id=category_id))

        for slug in item["section_slugs"]:
            section_id = section_slug_to_id.get(slug)
            if not section_id:
                continue
            exists = await db.scalar(
                select(func.count())
                .select_from(ProductSection)
                .where(
                    ProductSection.product_id == product.id,
                    ProductSection.section_id == section_id,
                )
            )
            if not exists:
                db.add(ProductSection(product_id=product.id, section_id=section_id))
