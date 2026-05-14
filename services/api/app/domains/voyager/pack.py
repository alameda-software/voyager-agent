from __future__ import annotations

import json

from app.domains.base import DomainReply
from app.models import ConciergeDomain

FUNCTIONS = [
    {
        "name": "search_flights",
        "description": "Search for available flights when you have enough info (origin, destination, approximate date, number of travellers).",
        "parameters": {
            "type": "object",
            "properties": {
                "origin": {"type": "string", "description": "Origin city or airport"},
                "destination": {"type": "string", "description": "Destination city or airport"},
                "date": {"type": "string", "description": "Travel date or month, e.g. 'June 2026' or '2026-06-15'"},
                "adults": {"type": "integer", "description": "Number of adult passengers"},
                "children": {"type": "integer", "description": "Number of child passengers"},
            },
            "required": ["origin", "destination"],
        },
    }
]

SYSTEM_PROMPT = """You are Voyager, a friendly AI travel concierge.
Help the user plan their perfect trip step by step.
Ask one focused follow-up question at a time to gather: origin, destination, dates, number of travellers, budget, and preferences.
Once you have origin + destination + rough dates + traveller count, call search_flights to show real options.
After showing flights, help with hotels, activities, and itinerary.
Be concise, warm, and helpful. Never repeat yourself. Keep replies under 3 sentences unless showing options."""


class VoyagerPack:
    domain = ConciergeDomain.VOYAGER

    def initial_state(self, title: str) -> dict:
        return {
            "title": title,
            "status": "collecting_requirements",
            "notes": [],
            "origin": None,
            "destination": None,
            "dates": None,
            "travellers": {"adults": 1, "children": 0},
            "budget": None,
            "flights_shown": False,
        }

    def merge_state(self, state: dict, user_message: str) -> dict:
        notes = list(state.get("notes", []))
        notes.append(user_message.strip())
        return {**state, "notes": notes[-30:]}

    def agent_reply(self, state: dict) -> DomainReply:
        from app.config import settings
        from app.services.fake_data import search_flights
        from openai import OpenAI

        notes = state.get("notes", [])
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for i, note in enumerate(notes):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append({"role": role, "content": note})

        client = OpenAI(api_key=settings.openai_api_key)

        try:
            response = client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                functions=FUNCTIONS,
                function_call="auto",
                max_tokens=400,
                temperature=0.7,
            )
            msg = response.choices[0].message

            # GPT wants to search flights
            if msg.function_call and msg.function_call.name == "search_flights":
                args = json.loads(msg.function_call.arguments)
                flights = search_flights(
                    origin=args.get("origin", ""),
                    destination=args.get("destination", ""),
                    date=args.get("date"),
                    adults=args.get("adults", 1),
                    children=args.get("children", 0),
                )

                # Feed results back to GPT for a natural summary
                messages.append({"role": "assistant", "content": None, "function_call": {
                    "name": "search_flights", "arguments": msg.function_call.arguments
                }})
                messages.append({
                    "role": "function",
                    "name": "search_flights",
                    "content": json.dumps(flights[:4]),
                })
                follow_up = client.chat.completions.create(
                    model=settings.llm_model,
                    messages=messages,
                    max_tokens=250,
                    temperature=0.7,
                )
                reply_text = follow_up.choices[0].message.content.strip()

                return DomainReply(
                    content=reply_text,
                    payload={
                        "mode": "flight_results",
                        "domain": self.domain.value,
                        "cards": flights[:4],
                    },
                )

            reply_text = msg.content.strip() if msg.content else "Let me help you plan your trip. Where would you like to go?"

        except Exception as e:
            reply_text = f"Sorry, I had a connection issue. Please try again. ({e})"

        return DomainReply(
            content=reply_text,
            payload={"mode": "llm", "domain": self.domain.value},
        )


voyager_pack = VoyagerPack()
