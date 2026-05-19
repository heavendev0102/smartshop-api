"""add products categories and product_categories tables

Revision ID: b2f8a1c3d4e5
Revises: a9a5cb6504e2
Create Date: 2026-05-18 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b2f8a1c3d4e5"
down_revision: Union[str, Sequence[str], None] = "a9a5cb6504e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
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
    op.create_index("ix_categories_slug", "categories", ["slug"])

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("current_price", sa.Numeric(10, 2), nullable=False),
        sa.Column("original_price", sa.Numeric(10, 2), nullable=True),
        sa.Column("discount_percent", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("modified_date", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "product_categories",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("created_date", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["category_id"], ["categories.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("product_id", "category_id", name="uq_product_category"),
    )
    op.create_index("ix_product_categories_product_id", "product_categories", ["product_id"])
    op.create_index("ix_product_categories_category_id", "product_categories", ["category_id"])

    categories = sa.table(
        "categories",
        sa.column("name", sa.String),
        sa.column("slug", sa.String),
        sa.column("description", sa.String),
        sa.column("display_order", sa.Integer),
        sa.column("is_active", sa.Boolean),
    )
    op.bulk_insert(
        categories,
        [
            {
                "name": "New Arrivals",
                "slug": "new_arrivals",
                "description": "Latest products",
                "display_order": 1,
                "is_active": True,
            },
            {
                "name": "Bestsellers",
                "slug": "bestsellers",
                "description": "Top selling products",
                "display_order": 2,
                "is_active": True,
            },
            {
                "name": "Featured",
                "slug": "featured",
                "description": "Highlighted products",
                "display_order": 3,
                "is_active": True,
            },
        ],
    )

    op.execute(
        """
        INSERT INTO products (name, image_url, current_price, original_price, discount_percent, is_active)
        VALUES
            ('Apple iPhone 14 Pro Max 128GB Deep Purple', 'https://placehold.co/600x600/ede9fe/5b21b6?text=iPhone+14+Pro', 810.00, 900.00, 10, true),
            ('Apple AirPods Max Over-Ear Headphones - Space Gray', 'https://placehold.co/600x600/f3f4f6/374151?text=AirPods+Max', 299.00, 599.00, 50, true),
            ('Samsung Galaxy Watch6 Classic 47mm Black', 'https://placehold.co/600x600/e0e7ff/312e81?text=Galaxy+Watch6', 249.00, 329.00, 24, true),
            ('Apple iPad 9 10.2 64GB Wi-Fi Silver (MK2L3) 2021', 'https://placehold.co/600x600/f5f5f4/44403c?text=iPad+9', 279.00, 329.00, 15, true)
        """
    )

    product_category_pairs = [
        ("Apple iPhone 14 Pro Max 128GB Deep Purple", "new_arrivals"),
        ("Apple iPhone 14 Pro Max 128GB Deep Purple", "featured"),
        ("Apple AirPods Max Over-Ear Headphones - Space Gray", "new_arrivals"),
        ("Apple AirPods Max Over-Ear Headphones - Space Gray", "bestsellers"),
        ("Samsung Galaxy Watch6 Classic 47mm Black", "bestsellers"),
        ("Samsung Galaxy Watch6 Classic 47mm Black", "featured"),
        ("Apple iPad 9 10.2 64GB Wi-Fi Silver (MK2L3) 2021", "new_arrivals"),
        ("Apple iPad 9 10.2 64GB Wi-Fi Silver (MK2L3) 2021", "bestsellers"),
        ("Apple iPad 9 10.2 64GB Wi-Fi Silver (MK2L3) 2021", "featured"),
    ]
    connection = op.get_bind()
    link_sql = sa.text(
        """
        INSERT INTO product_categories (product_id, category_id)
        SELECT p.id, c.id
        FROM products p, categories c
        WHERE p.name = :product_name AND c.slug = :category_slug
        """
    )
    for product_name, category_slug in product_category_pairs:
        connection.execute(
            link_sql,
            {"product_name": product_name, "category_slug": category_slug},
        )


def downgrade() -> None:
    op.drop_table("product_categories")
    op.drop_table("products")
    op.drop_index("ix_categories_slug", table_name="categories")
    op.drop_table("categories")
