from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ConciergeDomain(str, Enum):
    VOYAGER = "voyager"
    WEDDING = "wedding"


concierge_domain_type = SqlEnum(
    ConciergeDomain,
    name="conciergedomain",
    values_callable=lambda enum_cls: [member.value for member in enum_cls],
)


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    domain: Mapped[ConciergeDomain] = mapped_column(concierge_domain_type, index=True)
    title: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"))
    role: Mapped[str] = mapped_column(String(20))  # "user" | "agent" | "system"
    content: Mapped[str]
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # cards, buttons, and UI hints
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class StructuredState(Base):
    __tablename__ = "structured_states"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), unique=True, index=True)
    domain: Mapped[ConciergeDomain] = mapped_column(concierge_domain_type, index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class GeneratedDocument(Base):
    __tablename__ = "generated_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), index=True)
    domain: Mapped[ConciergeDomain] = mapped_column(concierge_domain_type, index=True)
    document_type: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str]
    payload: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class SavedRecommendation(Base):
    __tablename__ = "saved_recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), index=True)
    domain: Mapped[ConciergeDomain] = mapped_column(concierge_domain_type, index=True)
    category: Mapped[str] = mapped_column(String(100))
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PendingConfirmation(Base):
    __tablename__ = "pending_confirmations"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"), index=True)
    domain: Mapped[ConciergeDomain] = mapped_column(concierge_domain_type, index=True)
    action_type: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50), default="pending")
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
