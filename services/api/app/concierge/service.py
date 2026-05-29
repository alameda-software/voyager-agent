from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains import get_domain_pack
from app.models import ConciergeDomain, Conversation, Message, StructuredState, User
from app.schemas.chat import (
    ConversationCreate,
    ConversationDetail,
    ConversationSummary,
    MessageRead,
    SendMessageResponse,
    StructuredStateRead,
)


class ConciergeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_conversation(self, data: ConversationCreate) -> ConversationDetail:
        await self._ensure_user_exists(data.user_id)
        now = datetime.utcnow()

        conversation = Conversation(
            user_id=data.user_id,
            domain=data.domain,
            title=data.title.strip(),
            created_at=now,
        )
        self.db.add(conversation)
        await self.db.flush()

        structured_state = StructuredState(
            conversation_id=conversation.id,
            domain=data.domain,
            payload=get_domain_pack(data.domain).initial_state(data.title),
            created_at=now,
            updated_at=now,
        )
        self.db.add(structured_state)
        await self.db.commit()

        await self.db.refresh(conversation)
        await self.db.refresh(structured_state)

        return ConversationDetail(
            conversation=self._conversation_summary(conversation),
            structured_state=self._structured_state_read(structured_state),
            messages=[],
        )

    async def list_conversations(
        self,
        user_id: int,
        domain: ConciergeDomain | None = None,
    ) -> list[ConversationSummary]:
        query = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at.desc())
        if domain is not None:
            query = query.where(Conversation.domain == domain)

        result = await self.db.execute(query)
        conversations = result.scalars().all()
        return [self._conversation_summary(item) for item in conversations]

    async def get_conversation_detail(self, conversation_id: int) -> ConversationDetail:
        conversation = await self._get_conversation(conversation_id)
        structured_state = await self._get_or_create_state(conversation)
        messages = await self._get_messages(conversation_id)

        return ConversationDetail(
            conversation=self._conversation_summary(conversation),
            structured_state=self._structured_state_read(structured_state),
            messages=[self._message_read(item) for item in messages],
        )

    async def send_message(self, conversation_id: int, content: str) -> SendMessageResponse:
        conversation = await self._get_conversation(conversation_id)
        structured_state = await self._get_or_create_state(conversation)
        now = datetime.utcnow()

        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=content.strip(),
            payload=None,
            created_at=now,
        )
        self.db.add(user_message)
        await self.db.flush()

        # Get full message history BEFORE this new message for context
        existing_messages = await self._get_messages(conversation_id)
        history = [
            {"role": "user" if m.role == "user" else "assistant", "content": m.content}
            for m in existing_messages
            if m.role in ("user", "agent") and m.content
        ]
        # Append current user message
        history.append({"role": "user", "content": content.strip()})

        structured_state.payload = self._merge_state(
            domain=conversation.domain,
            state=structured_state.payload,
            user_message=content,
        )
        structured_state.updated_at = now

        agent_reply = self._agent_reply(
            domain=conversation.domain,
            state=structured_state.payload,
            history=history,
        )
        agent_message = Message(
            conversation_id=conversation.id,
            role="agent",
            content=agent_reply.content,
            payload=agent_reply.payload,
            created_at=now,
        )
        self.db.add(agent_message)
        await self.db.commit()

        await self.db.refresh(conversation)
        await self.db.refresh(structured_state)
        await self.db.refresh(user_message)
        await self.db.refresh(agent_message)

        return SendMessageResponse(
            conversation=self._conversation_summary(conversation),
            structured_state=self._structured_state_read(structured_state),
            user_message=self._message_read(user_message),
            agent_message=self._message_read(agent_message),
        )

    async def get_history(self, conversation_id: int) -> list[MessageRead]:
        await self._get_conversation(conversation_id)
        messages = await self._get_messages(conversation_id)
        return [self._message_read(item) for item in messages]

    async def delete_conversation(self, conversation_id: int) -> dict:
        conversation = await self._get_conversation(conversation_id)
        self.db.delete(conversation)
        await self.db.commit()
        return {"success": True}

    async def _ensure_user_exists(self, user_id: int) -> User:
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is not None:
            return user

        user = User(
            id=user_id,
            email=f"guest-{user_id}@voyager.local",
            hashed_password="guest-user",
            is_active=True,
            display_name=f"Guest {user_id}",
        )
        self.db.add(user)
        await self.db.flush()
        return user

    async def _get_conversation(self, conversation_id: int) -> Conversation:
        result = await self.db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = result.scalar_one_or_none()
        if conversation is None:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return conversation

    async def _get_or_create_state(self, conversation: Conversation) -> StructuredState:
        result = await self.db.execute(
            select(StructuredState).where(StructuredState.conversation_id == conversation.id)
        )
        structured_state = result.scalar_one_or_none()
        if structured_state is not None:
            return structured_state

        structured_state = StructuredState(
            conversation_id=conversation.id,
            domain=conversation.domain,
            payload=get_domain_pack(conversation.domain).initial_state(conversation.title),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.db.add(structured_state)
        await self.db.commit()
        await self.db.refresh(structured_state)
        return structured_state

    async def _get_messages(self, conversation_id: int) -> Iterable[Message]:
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc(), Message.id.asc())
        )
        return result.scalars().all()

    def _initial_state(self, domain: ConciergeDomain, title: str) -> dict:
        return get_domain_pack(domain).initial_state(title)

    def _merge_state(self, domain: ConciergeDomain, state: dict, user_message: str) -> dict:
        return get_domain_pack(domain).merge_state(state, user_message)

    def _agent_reply(self, domain: ConciergeDomain, state: dict, history: list | None = None):
        return get_domain_pack(domain).agent_reply(state, history=history or [])

    def _conversation_summary(self, conversation: Conversation) -> ConversationSummary:
        return ConversationSummary(
            id=conversation.id,
            user_id=conversation.user_id,
            domain=conversation.domain,
            title=conversation.title,
            created_at=conversation.created_at,
        )

    def _structured_state_read(self, structured_state: StructuredState) -> StructuredStateRead:
        return StructuredStateRead(
            conversation_id=structured_state.conversation_id,
            domain=structured_state.domain,
            payload=structured_state.payload,
            updated_at=structured_state.updated_at,
        )

    def _message_read(self, message: Message) -> MessageRead:
        return MessageRead(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
            payload=message.payload,
            created_at=message.created_at,
        )
