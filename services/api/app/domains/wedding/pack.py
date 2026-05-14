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
        next_state = {**state, "notes": notes[-20:]}
        next_state["event_request"] = user_message.strip()
        return next_state

    def agent_reply(self, state: dict) -> DomainReply:
        from app.config import settings
        from openai import OpenAI

        notes = state.get("notes", [])
        system_prompt = (
            "You are a warm, experienced wedding planning concierge. "
            "Help the user plan their perfect wedding. "
            "Ask one focused follow-up question at a time to gather: location, date, guest count, "
            "budget, and priority vendors (venue, catering, music, photography, flowers). "
            "Once you have enough info, suggest vendor options and planning milestones. "
            "Be warm, celebratory, and practical. Never repeat yourself."
        )

        messages = [{"role": "system", "content": system_prompt}]
        for i, note in enumerate(notes):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": note})

        try:
            client = OpenAI(api_key=settings.openai_api_key)
            response = client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                max_tokens=300,
                temperature=0.7,
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"I'm having trouble connecting right now. Please try again. ({e})"

        return DomainReply(
            content=reply,
            payload={"mode": "llm", "domain": self.domain.value},
        )


wedding_pack = WeddingPack()
