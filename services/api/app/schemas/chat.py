from datetime import datetime

from pydantic import BaseModel, Field

from app.models import ConciergeDomain


class ConversationCreate(BaseModel):
    user_id: int
    domain: ConciergeDomain
    title: str = Field(min_length=1, max_length=255)


class ConversationSummary(BaseModel):
    id: int
    user_id: int
    domain: ConciergeDomain
    title: str
    created_at: datetime


class MessageRead(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    payload: dict | None
    created_at: datetime


class StructuredStateRead(BaseModel):
    conversation_id: int
    domain: ConciergeDomain
    payload: dict
    updated_at: datetime


class ConversationDetail(BaseModel):
    conversation: ConversationSummary
    structured_state: StructuredStateRead
    messages: list[MessageRead]


class SendMessageRequest(BaseModel):
    conversation_id: int
    content: str = Field(min_length=1)


class SendMessageResponse(BaseModel):
    conversation: ConversationSummary
    structured_state: StructuredStateRead
    user_message: MessageRead
    agent_message: MessageRead
