"""Shared helpers for Alembic migrations and seed data."""

from app.db.seed_data import DEFAULT_CATEGORIES, DEFAULT_SECTIONS, DUMMY_PRODUCTS


def get_sync_database_url(database_url: str) -> str:
    """Alembic needs a sync driver URL (psycopg2), not asyncpg."""
    if database_url.startswith("postgresql+asyncpg://"):
        return database_url.replace("postgresql+asyncpg://", "postgresql://", 1)
    if database_url.startswith("postgres+asyncpg://"):
        return database_url.replace("postgres+asyncpg://", "postgresql://", 1)
    return database_url


def migration_browse_categories() -> list[tuple]:
    """(name, slug, description, icon_url, display_order)"""
    return [
        (
            item["name"],
            item["slug"],
            item.get("description"),
            item.get("icon_url"),
            item["display_order"],
        )
        for item in DEFAULT_CATEGORIES
    ]


def migration_sections() -> list[tuple]:
    """(name, slug, description, display_order)"""
    return [
        (
            item["name"],
            item["slug"],
            item.get("description"),
            item["display_order"],
        )
        for item in DEFAULT_SECTIONS
    ]


def migration_product_links() -> list[tuple]:
    """(product_name, category_slug, section_slugs)"""
    return [
        (
            item["name"],
            item["category_slugs"][0],
            item["section_slugs"],
        )
        for item in DUMMY_PRODUCTS
    ]
