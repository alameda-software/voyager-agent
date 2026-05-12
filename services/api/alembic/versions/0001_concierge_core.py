"""initial concierge core schema

Revision ID: 0001_concierge_core
Revises: None
Create Date: 2026-05-06 23:40:00.000000
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_concierge_core"
down_revision = None
branch_labels = None
depends_on = None


concierge_domain_enum = sa.Enum("voyager", "wedding", name="conciergedomain")


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("display_name", sa.String(), nullable=True),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "conversations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("domain", concierge_domain_enum, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_conversations_domain", "conversations", ["domain"], unique=False)

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "structured_states",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("domain", concierge_domain_enum, nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_structured_states_conversation_id", "structured_states", ["conversation_id"], unique=True)
    op.create_index("ix_structured_states_domain", "structured_states", ["domain"], unique=False)

    op.create_table(
        "generated_documents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("domain", concierge_domain_enum, nullable=False),
        sa.Column("document_type", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_generated_documents_conversation_id", "generated_documents", ["conversation_id"], unique=False)
    op.create_index("ix_generated_documents_domain", "generated_documents", ["domain"], unique=False)

    op.create_table(
        "saved_recommendations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("domain", concierge_domain_enum, nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_saved_recommendations_conversation_id", "saved_recommendations", ["conversation_id"], unique=False)
    op.create_index("ix_saved_recommendations_domain", "saved_recommendations", ["domain"], unique=False)

    op.create_table(
        "pending_confirmations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("conversation_id", sa.Integer(), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("domain", concierge_domain_enum, nullable=False),
        sa.Column("action_type", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="pending"),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_pending_confirmations_conversation_id", "pending_confirmations", ["conversation_id"], unique=False)
    op.create_index("ix_pending_confirmations_domain", "pending_confirmations", ["domain"], unique=False)


def downgrade():
    op.drop_index("ix_pending_confirmations_domain", table_name="pending_confirmations")
    op.drop_index("ix_pending_confirmations_conversation_id", table_name="pending_confirmations")
    op.drop_table("pending_confirmations")

    op.drop_index("ix_saved_recommendations_domain", table_name="saved_recommendations")
    op.drop_index("ix_saved_recommendations_conversation_id", table_name="saved_recommendations")
    op.drop_table("saved_recommendations")

    op.drop_index("ix_generated_documents_domain", table_name="generated_documents")
    op.drop_index("ix_generated_documents_conversation_id", table_name="generated_documents")
    op.drop_table("generated_documents")

    op.drop_index("ix_structured_states_domain", table_name="structured_states")
    op.drop_index("ix_structured_states_conversation_id", table_name="structured_states")
    op.drop_table("structured_states")

    op.drop_table("messages")

    op.drop_index("ix_conversations_domain", table_name="conversations")
    op.drop_table("conversations")

    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
