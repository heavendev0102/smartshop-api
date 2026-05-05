"""add missing users table

Revision ID: ced5809b0f1d
Revises: a9a5cb6504e2
Create Date: 2026-05-04 17:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ced5809b0f1d'
down_revision: Union[str, Sequence[str], None] = 'a9a5cb6504e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('username', sa.String(length=100), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('gender', sa.String(length=10), nullable=True),
        sa.Column('date_of_birth', sa.DateTime(timezone=True), nullable=True),
        sa.Column('profile_image', sa.String(), nullable=True),
        sa.Column('password_hash', sa.String(), nullable=True),
        sa.Column('email_confirmed', sa.Boolean(), nullable=True),
        sa.Column('phone_number_confirmed', sa.Boolean(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('modified_date', sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email'),
    )


def downgrade() -> None:
    op.drop_table('users')
