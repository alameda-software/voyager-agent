from __future__ import annotations

import json

from app.domains.base import DomainReply
from app.models import ConciergeDomain

FUNCTIONS = [
    {
        "name": "search_vendors",
        "description": "Search for wedding vendors when you have location + guest count + at least one category needed.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Vendor category: venue, catering, photography, music, or all",
                    "enum": ["all", "venue", "catering", "photography", "music"],
                },
                "location": {"type": "string", "description": "Wedding location city"},
                "guest_count": {"type": "integer", "description": "Estimated number of guests"},
                "budget": {"type": "integer", "description": "Total budget in EUR if known"},
            },
            "required": ["category", "location"],
        },
    }
]

SYSTEM_PROMPT = """You are a warm, experienced wedding planning concierge.
Help the user plan their perfect wedding step by step.
Ask one focused follow-up question at a time to gather: location, date, guest count, budget, and priority vendors (venue, catering, music, photography).
Once you have location + guest count + at least one vendor category, call search_vendors to show options.
After showing vendors, help with timeline, budget breakdown, and next steps.
Be warm, celebratory, and practical. Keep replies under 3 sentences unless showing options. Never repeat yourself."""


class WeddingPack:
    domain = ConciergeDomain.WEDDING

    def initial_state(self, title: str) -> dict:
        return {
            "title": title,
            "status": "collecting_requirements",
            "notes": [],
            "location": None,
            "event_date": None,
            "guest_count": None,
            "budget": None,
            "vendors_needed": [],
        }

    def merge_state(self, state: dict, user_message: str) -> dict:
        return {**state}  # History-driven now

    def agent_reply(self, state: dict, history: list | None = None) -> DomainReply:
        from app.config import settings
        from app.services.fake_data import search_vendors
        from openai import OpenAI

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in (history or []):
            messages.append({"role": msg["role"], "content": msg["content"]})

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

            # GPT wants to search vendors
            if msg.function_call and msg.function_call.name == "search_vendors":
                args = json.loads(msg.function_call.arguments)
                vendors = search_vendors(
                    category=args.get("category", "all"),
                    location=args.get("location", "Seville"),
                    guest_count=args.get("guest_count", 100),
                    budget=args.get("budget"),
                )

                messages.append({"role": "assistant", "content": None, "function_call": {
                    "name": "search_vendors", "arguments": msg.function_call.arguments
                }})
                messages.append({
                    "role": "function",
                    "name": "search_vendors",
                    "content": json.dumps(vendors[:6]),
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
                        "mode": "vendor_results",
                        "domain": self.domain.value,
                        "cards": vendors[:6],
                    },
                )

            reply_text = msg.content.strip() if msg.content else "I'd love to help plan your wedding! Where are you thinking of holding it?"

        except Exception as e:
            reply_text = f"Sorry, I had a connection issue. Please try again. ({e})"

        return DomainReply(
            content=reply_text,
            payload={"mode": "llm", "domain": self.domain.value},
        )


wedding_pack = WeddingPack()
