from fastapi import APIRouter
from pydantic import BaseModel

from app.services.agents.travel_agent import TravelAgent

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_id: int | None = None


class ChatResponse(BaseModel):
    role: str
    content: str
    metadata: dict | None = None


@router.post("/send", response_model=ChatResponse)
async def send_message(req: ChatRequest):
    """Send a message to the travel agent and get a response."""
    agent = TravelAgent()
    result = await agent.process_message(
        message=req.message,
        conversation_id=req.conversation_id or 0,
    )
    return ChatResponse(**result)


@router.get("/history")
async def get_history(conversation_id: int = 0):
    """Get conversation history."""
    # TODO: fetch from database
    return {"messages": []}
