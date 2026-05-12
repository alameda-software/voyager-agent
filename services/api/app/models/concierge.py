"""
Shared concierge persistence models live here so domain logic can evolve
independently and later move into separate repos with minimal coupling.
"""

from app.models.conversation import (
    ConciergeDomain,
    Conversation,
    GeneratedDocument,
    Message,
    PendingConfirmation,
    SavedRecommendation,
    StructuredState,
)

__all__ = [
    "ConciergeDomain",
    "Conversation",
    "GeneratedDocument",
    "Message",
    "PendingConfirmation",
    "SavedRecommendation",
    "StructuredState",
]
