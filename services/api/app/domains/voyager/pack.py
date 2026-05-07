from app.domains.base import DomainReply
from app.models import ConciergeDomain


class VoyagerPack:
    domain = ConciergeDomain.VOYAGER

    def initial_state(self, title: str) -> dict:
        return {
            "title": title,
            "status": "collecting_requirements",
            "notes": [],
            "trip_request": None,
            "origin": None,
            "destination": None,
            "dates": {"start": None, "end": None, "flexibility": None},
            "travellers": {"total": None, "adults": None, "children": None},
            "budget": None,
            "preferences": [],
            "next_questions": [
                "When would you like to travel?",
                "How many travellers are going?",
                "What budget range should I optimize for?",
            ],
        }

    def merge_state(self, state: dict, user_message: str) -> dict:
        notes = list(state.get("notes", []))
        notes.append(user_message.strip())
        next_state = {**state, "notes": notes[-12:]}
        next_state["trip_request"] = user_message.strip()
        return next_state

    def agent_reply(self, state: dict) -> DomainReply:
        questions = state.get("next_questions", [])
        prompt = questions[0] if questions else "Tell me the most important remaining travel constraint."
        return DomainReply(
            content=(
                "I’ve saved your trip request and opened a Voyager planning session. "
                f"Next, I need one key detail: {prompt}"
            ),
            payload={
                "mode": "pre_mvp_fake_data",
                "domain": self.domain.value,
                "suggested_actions": [
                    "collect_trip_requirements",
                    "prepare_fake_search",
                ],
            },
        )


voyager_pack = VoyagerPack()
