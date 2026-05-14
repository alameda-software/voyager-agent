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
        next_state = {**state, "notes": notes[-20:]}
        next_state["trip_request"] = user_message.strip()
        return next_state

    def agent_reply(self, state: dict) -> DomainReply:
        # Lazy import to avoid circular deps
        from app.config import settings
        from openai import OpenAI

        notes = state.get("notes", [])
        system_prompt = (
            "You are Voyager, a friendly AI travel concierge. "
            "Help the user plan their perfect trip. "
            "Ask one focused follow-up question at a time to gather: origin, destination, dates, "
            "number of travellers, budget, and preferences. "
            "Once you have enough info, suggest flight options and itinerary ideas. "
            "Be concise, warm, and helpful. Never repeat yourself."
        )

        # Build message history from notes
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


voyager_pack = VoyagerPack()
