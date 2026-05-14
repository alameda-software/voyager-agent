from __future__ import annotations

import json

from app.domains.base import DomainReply
from app.models import ConciergeDomain

FUNCTIONS = [
    {
        "name": "search_flights",
        "description": "Search flights when you have origin, destination, and approximate dates.",
        "parameters": {
            "type": "object",
            "properties": {
                "origin": {"type": "string", "description": "Origin city or airport"},
                "destination": {"type": "string", "description": "Destination city or airport"},
                "date": {"type": "string", "description": "Travel date or month"},
                "adults": {"type": "integer"},
                "children": {"type": "integer"},
            },
            "required": ["origin", "destination"],
        },
    },
    {
        "name": "search_hotels",
        "description": "Search hotels at the destination when you know where and roughly when.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {"type": "string", "description": "City or destination"},
                "checkin": {"type": "string", "description": "Check-in date"},
                "checkout": {"type": "string", "description": "Check-out date"},
                "nights": {"type": "integer", "description": "Number of nights"},
                "adults": {"type": "integer"},
                "children": {"type": "integer"},
            },
            "required": ["destination"],
        },
    },
    {
        "name": "search_car_rentals",
        "description": "Search car rentals at the destination when the user needs a car.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "Pickup city or airport"},
                "pickup_date": {"type": "string"},
                "dropoff_date": {"type": "string"},
                "days": {"type": "integer", "description": "Number of rental days"},
                "category": {"type": "string", "description": "economy, compact, suv, premium, family"},
            },
            "required": ["location"],
        },
    },
]

SYSTEM_PROMPT = """You are Voyager, a friendly AI travel concierge.
Help the user plan their perfect trip step by step.
Gather: origin, destination, dates, number of travellers, budget, and whether they need a hotel or car.
- Once you have origin + destination + dates + travellers → call search_flights
- Once you know destination + dates → offer to call search_hotels
- If user mentions needing a car → call search_car_rentals
IMPORTANT: When you call a search function, the results will be shown as visual cards to the user.
DO NOT list the results as numbered text — just write a short 1-2 sentence intro and ask what they need next.
Example good response after flights: "Here are the best options for your trip! Would you also like hotels or a rental car?"
Be concise and warm. Never repeat yourself."""


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
            "needs_hotel": None,
            "needs_car": None,
        }

    def merge_state(self, state: dict, user_message: str) -> dict:
        notes = list(state.get("notes", []))
        notes.append(user_message.strip())
        return {**state, "notes": notes[-30:]}

    def agent_reply(self, state: dict) -> DomainReply:
        from app.config import settings
        from app.services.fake_data import search_flights, search_hotels, search_car_rentals
        from openai import OpenAI

        notes = state.get("notes", [])
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for i, note in enumerate(notes):
            messages.append({"role": "user" if i % 2 == 0 else "assistant", "content": note})

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

            if msg.function_call:
                fn = msg.function_call.name
                args = json.loads(msg.function_call.arguments)

                if fn == "search_flights":
                    cards = search_flights(
                        origin=args.get("origin", ""),
                        destination=args.get("destination", ""),
                        date=args.get("date"),
                        adults=args.get("adults", 1),
                        children=args.get("children", 0),
                    )
                    mode = "flight_results"
                elif fn == "search_hotels":
                    cards = search_hotels(
                        destination=args.get("destination", ""),
                        checkin=args.get("checkin"),
                        checkout=args.get("checkout"),
                        nights=args.get("nights", 3),
                        adults=args.get("adults", 1),
                        children=args.get("children", 0),
                    )
                    mode = "hotel_results"
                elif fn == "search_car_rentals":
                    cards = search_car_rentals(
                        location=args.get("location", ""),
                        pickup_date=args.get("pickup_date"),
                        dropoff_date=args.get("dropoff_date"),
                        days=args.get("days", 3),
                        category=args.get("category"),
                    )
                    mode = "car_results"
                else:
                    cards, mode = [], "llm"

                # Feed results back for natural summary
                messages.append({"role": "assistant", "content": None,
                                  "function_call": {"name": fn, "arguments": msg.function_call.arguments}})
                messages.append({"role": "function", "name": fn, "content": json.dumps(cards[:4])})
                follow_up = client.chat.completions.create(
                    model=settings.llm_model, messages=messages,
                    max_tokens=250, temperature=0.7,
                )
                reply_text = follow_up.choices[0].message.content.strip()
                return DomainReply(
                    content=reply_text,
                    payload={"mode": mode, "domain": self.domain.value, "cards": cards[:4]},
                )

            reply_text = msg.content.strip() if msg.content else "¿A dónde te gustaría viajar?"

        except Exception as e:
            reply_text = f"Tengo un problema de conexión. Inténtalo de nuevo. ({e})"

        return DomainReply(content=reply_text, payload={"mode": "llm", "domain": self.domain.value})


voyager_pack = VoyagerPack()
