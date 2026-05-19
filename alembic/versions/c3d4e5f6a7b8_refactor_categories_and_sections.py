"""refactor browse categories and add product sections

Revision ID: c3d4e5f6a7b8
Revises: b2f8a1c3d4e5
Create Date: 2026-05-18 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.db.migration_common import (
    migration_browse_categories,
    migration_product_links,
    migration_sections,
)


revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, Sequence[str], None] = "b2f8a1c3d4e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

BROWSE_CATEGORIES = migration_browse_categories()
SECTIONS = migration_sections()
PRODUCT_LINKS = migration_product_links()


def upgrade() -> None:
    op.add_column("categories", sa.Column("icon_url", sa.String(), nullable=True))

    op.create_table(
        "sections",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("modified_date", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index("ix_sections_slug", "sections", ["slug"])

    op.create_table(
        "product_sections",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.Column("created_date", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["section_id"], ["sections.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("product_id", "section_id", name="uq_product_section"),
    )

    op.execute("DELETE FROM product_categories")
    op.execute("DELETE FROM categories")

    connection = op.get_bind()
    for name, slug, description, icon_url, display_order in BROWSE_CATEGORIES:
        connection.execute(
            sa.text(
                """
                INSERT INTO categories (name, slug, description, icon_url, display_order, is_active)
                VALUES (:name, :slug, :description, :icon_url, :display_order, true)
                """
            ),
            {
                "name": name,
                "slug": slug,
                "description": description,
                "icon_url": icon_url,
                "display_order": display_order,
            },
        )

    for name, slug, description, display_order in SECTIONS:
        connection.execute(
            sa.text(
                """
                INSERT INTO sections (name, slug, description, display_order, is_active)
                VALUES (:name, :slug, :description, :display_order, true)
                """
            ),
            {
                "name": name,
                "slug": slug,
                "description": description,
                "display_order": display_order,
            },
        )

    link_category_sql = sa.text(
        """
        INSERT INTO product_categories (product_id, category_id)
        SELECT p.id, c.id FROM products p, categories c
        WHERE p.name = :product_name AND c.slug = :category_slug
        """
    )
    link_section_sql = sa.text(
        """
        INSERT INTO product_sections (product_id, section_id)
        SELECT p.id, s.id FROM products p, sections s
        WHERE p.name = :product_name AND s.slug = :section_slug
        """
    )
    for product_name, category_slug, section_slugs in PRODUCT_LINKS:
        connection.execute(
            link_category_sql,
            {"product_name": product_name, "category_slug": category_slug},
        )
        for section_slug in section_slugs:
            connection.execute(
                link_section_sql,
                {"product_name": product_name, "section_slug": section_slug},
            )


def downgrade() -> None:
    op.execute("DELETE FROM product_sections")
    op.drop_table("product_sections")
    op.drop_index("ix_sections_slug", table_name="sections")
    op.drop_table("sections")
    op.drop_column("categories", "icon_url")
