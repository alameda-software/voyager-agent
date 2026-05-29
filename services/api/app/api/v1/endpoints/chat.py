from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.concierge.service import ConciergeService
from app.db.session import get_db
from app.models import ConciergeDomain
from app.schemas.chat import (
    ConversationCreate,
    ConversationDetail,
    ConversationSummary,
    MessageRead,
    SendMessageRequest,
    SendMessageResponse,
)

router = APIRouter()


@router.post("/conversations", response_model=ConversationDetail)
async def create_conversation(
    payload: ConversationCreate,
    db: AsyncSession = Depends(get_db),
):
    service = ConciergeService(db)
    return await service.create_conversation(payload)


@router.get("/conversations", response_model=list[ConversationSummary])
async def list_conversations(
    user_id: int = Query(...),
    domain: ConciergeDomain | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    service = ConciergeService(db)
    return await service.list_conversations(user_id=user_id, domain=domain)


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = ConciergeService(db)
    return await service.get_conversation_detail(conversation_id)


@router.post("/send", response_model=SendMessageResponse)
async def send_message(
    payload: SendMessageRequest,
    db: AsyncSession = Depends(get_db),
):
    service = ConciergeService(db)
    return await service.send_message(
        conversation_id=payload.conversation_id,
        content=payload.content,
    )


@router.get("/history", response_model=list[MessageRead])
async def get_history(
    conversation_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    service = ConciergeService(db)
    return await service.get_history(conversation_id)


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = ConciergeService(db)
    return await service.delete_conversation(conversation_id)
