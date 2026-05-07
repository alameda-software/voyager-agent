from app.domains.base import DomainReply
from app.models import ConciergeDomain


class WeddingPack:
    domain = ConciergeDomain.WEDDING

    def initial_state(self, title: str) -> dict:
        return {
            "title": title,
            "status": "collecting_requirements",
            "notes": [],
            "event_request": None,
            "location": None,
            "event_date": None,
            "guest_count": None,
            "budget": None,
            "vendors_needed": [],
            "priorities": [],
            "next_questions": [
                "What date or season are you targeting?",
                "Roughly how many guests are you planning for?",
                "Which vendors matter most right now: venue, catering, music, or photo?",
            ],
        }

    def merge_state(self, state: dict, user_message: str) -> dict:
        notes = list(state.get("notes", []))
        notes.append(user_message.strip())
        next_state = {**state, "notes": notes[-12:]}
        next_state["event_request"] = user_message.strip()
        return next_state

    def agent_reply(self, state: dict) -> DomainReply:
        questions = state.get("next_questions", [])
        prompt = questions[0] if questions else "Tell me the biggest wedding-planning priority."
        return DomainReply(
            content=(
                "I’ve saved your wedding request and opened a Wedding planning session. "
                f"Next, I need one key detail: {prompt}"
            ),
            payload={
                "mode": "pre_mvp_fake_data",
                "domain": self.domain.value,
                "suggested_actions": [
                    "collect_wedding_requirements",
                    "prepare_fake_vendor_search",
                ],
            },
        )


wedding_pack = WeddingPack()
