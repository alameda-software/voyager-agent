"""Add wedding vendors table

Revision ID: 0002_wedding_vendors
Revises: 0001_concierge_core
Create Date: 2026-05-28 01:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0002_wedding_vendors"
down_revision = "0001_concierge_core"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "wedding_vendors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=50), nullable=False, index=True),
        sa.Column("category_label", sa.String(length=100), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False, index=True),
        sa.Column("region", sa.String(length=100), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("review_count", sa.Integer(), nullable=True),
        sa.Column("price_from", sa.Float(), nullable=True),
        sa.Column("price_label", sa.String(length=255), nullable=True),
        sa.Column("short_description", sa.Text(), nullable=True),
        sa.Column("tags", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("capacity_min", sa.Integer(), nullable=True),
        sa.Column("capacity_max", sa.Integer(), nullable=True),
        sa.Column("featured", sa.Boolean(), nullable=False, server_default=sa.text("false"), index=True),
        sa.Column("promotion", sa.Text(), nullable=True),
        sa.Column("availability_hint", sa.String(length=255), nullable=True),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_wedding_vendors_category_city", "wedding_vendors", ["category", "city"], unique=False)
    op.create_index("ix_wedding_vendors_featured", "wedding_vendors", ["featured"], unique=False)


def downgrade():
    op.drop_index("ix_wedding_vendors_featured", "wedding_vendors")
    op.drop_index("ix_wedding_vendors_category_city", "wedding_vendors")
    op.drop_table("wedding_vendors")
