from __future__ import annotations

import json

from app.domains.base import DomainReply
from app.models import ConciergeDomain

FUNCTIONS = [
    {
        "name": "search_flights",
        "description": "Search flights when you have origin, destination, and approximate dates. Only call this once unless the user asks to search again.",
        "parameters": {
            "type": "object",
            "properties": {
                "origin": {"type": "string"},
                "destination": {"type": "string"},
                "date": {"type": "string"},
                "adults": {"type": "integer"},
                "children": {"type": "integer"},
            },
            "required": ["origin", "destination"],
        },
    },
    {
        "name": "search_hotels",
        "description": "Search hotels at the destination.",
        "parameters": {
            "type": "object",
            "properties": {
                "destination": {"type": "string"},
                "checkin": {"type": "string"},
                "checkout": {"type": "string"},
                "nights": {"type": "integer"},
                "adults": {"type": "integer"},
                "children": {"type": "integer"},
            },
            "required": ["destination"],
        },
    },
    {
        "name": "search_car_rentals",
        "description": "Search car rentals when the user needs a car.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"},
                "pickup_date": {"type": "string"},
                "dropoff_date": {"type": "string"},
                "days": {"type": "integer"},
                "category": {"type": "string"},
            },
            "required": ["location"],
        },
    },
    {
        "name": "confirm_booking",
        "description": "Call this when the user selects a specific flight, hotel or car and wants to book it.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_type": {"type": "string", "enum": ["flight", "hotel", "car"]},
                "item_description": {"type": "string", "description": "e.g. 'easyJet 13:35 LHR-SVQ €139'"},
                "total_price": {"type": "number"},
                "currency": {"type": "string"},
            },
            "required": ["item_type", "item_description"],
        },
    },
]

SYSTEM_PROMPT = """You are Voyager, a friendly AI travel concierge.
Help the user plan their perfect trip conversationally.

Rules:
- Gather origin, destination, dates, travellers naturally through conversation
- Call search_flights once you have enough info. Do NOT call it again unless user asks.
- After showing flights, ask if they need hotels or a car
- Call search_hotels or search_car_rentals when needed
- When the user says they want to SELECT or BOOK a specific option (e.g. "I'll take the easyJet", "book the Volotea", "I want that hotel") → call confirm_booking
- After confirming a booking, congratulate them and ask what else they need
- Be warm, concise. Max 2 sentences unless showing options.
- NEVER re-list search results as text — the cards are shown visually."""


class VoyagerPack:
    domain = ConciergeDomain.VOYAGER

    def initial_state(self, title: str) -> dict:
        return {
            "title": title,
            "status": "collecting_requirements",
            "origin": None,
            "destination": None,
            "dates": None,
            "travellers": {"adults": 1, "children": 0},
            "budget": None,
            "bookings": [],
        }

    def merge_state(self, state: dict, user_message: str) -> dict:
        return {**state}  # State is now driven by history, not notes

    def agent_reply(self, state: dict, history: list | None = None) -> DomainReply:
        from app.config import settings
        from app.services.fake_data import search_flights, search_hotels, search_car_rentals
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
                elif fn == "confirm_booking":
                    item = args.get("item_description", "your selection")
                    price = args.get("total_price")
                    price_str = f" — €{price}" if price else ""
                    reply_text = f"✅ Perfect! I've noted your booking: **{item}**{price_str}. Would you like to add hotels, a car, or is there anything else for your trip?"
                    return DomainReply(
                        content=reply_text,
                        payload={"mode": "booking_confirmed", "domain": self.domain.value,
                                 "booking": args},
                    )
                else:
                    cards, mode = [], "llm"

                if fn in ("search_flights", "search_hotels", "search_car_rentals"):
                    messages.append({"role": "assistant", "content": None,
                                     "function_call": {"name": fn, "arguments": msg.function_call.arguments}})
                    messages.append({"role": "function", "name": fn, "content": json.dumps(cards[:4])})
                    follow_up = client.chat.completions.create(
                        model=settings.llm_model, messages=messages,
                        max_tokens=150, temperature=0.7,
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
