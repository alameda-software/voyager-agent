from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from app.models import ConciergeDomain


@dataclass(frozen=True)
class DomainReply:
    content: str
    payload: dict | None = None


class DomainPack(Protocol):
    domain: ConciergeDomain

    def initial_state(self, title: str) -> dict: ...

    def merge_state(self, state: dict, user_message: str) -> dict: ...

    def agent_reply(self, state: dict) -> DomainReply: ...
