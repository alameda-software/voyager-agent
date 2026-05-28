"""user roles and profile fields

Revision ID: 0003
Revises: 0002
Create Date: 2026-05-28
"""
from alembic import op
import sqlalchemy as sa

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('role', sa.String(50), nullable=False, server_default='user'))
    op.add_column('users', sa.Column('partner_name', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('wedding_date', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('city', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('budget', sa.Integer(), nullable=True))
    # Make display_name explicitly nullable
    op.alter_column('users', 'display_name', existing_type=sa.String(255), nullable=True)


def downgrade():
    op.drop_column('users', 'role')
    op.drop_column('users', 'partner_name')
    op.drop_column('users', 'wedding_date')
    op.drop_column('users', 'city')
    op.drop_column('users', 'budget')
