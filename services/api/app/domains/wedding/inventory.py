from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

from app.domains.wedding.categories import CATEGORY_ALIASES, CATEGORY_BY_ID, WEDDING_VENDOR_CATEGORIES

_DATA_PATH = Path(__file__).resolve().parent / "data" / "vendors.json"

CITY_ALIASES: dict[str, str] = {
    "sevilla": "Sevilla",
    "seville": "Sevilla",
    "madrid": "Madrid",
    "barcelona": "Barcelona",
    "malaga": "Málaga",
    "málaga": "Málaga",
    "valencia": "Valencia",
    "cadiz": "Cádiz",
    "cádiz": "Cádiz",
    "granada": "Granada",
    "cordoba": "Córdoba",
    "córdoba": "Córdoba",
}


def _normalize(text: str) -> str:
    lowered = text.lower().strip()
    normalized = unicodedata.normalize("NFD", lowered)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


@lru_cache(maxsize=1)
def load_vendors() -> list[dict]:
    if not _DATA_PATH.exists():
        return []
    payload = json.loads(_DATA_PATH.read_text(encoding="utf-8"))
    return list(payload.get("vendors", []))


def list_categories() -> list[dict]:
    return [
        {
            "id": item.id,
            "label": item.label,
            "description": item.description,
            "icon": item.icon,
            "bodas_path": item.bodas_path,
            "vendor_count": sum(1 for vendor in load_vendors() if vendor["category"] == item.id),
        }
        for item in WEDDING_VENDOR_CATEGORIES
    ]


def detect_category(text: str) -> str | None:
    normalized = _normalize(text)
    for alias, category_id in sorted(CATEGORY_ALIASES.items(), key=lambda item: -len(item[0])):
        if _normalize(alias) in normalized:
            return category_id
    for category in WEDDING_VENDOR_CATEGORIES:
        if _normalize(category.label) in normalized or category.id in normalized:
            return category.id
    return None


def detect_city(text: str) -> str | None:
    normalized = _normalize(text)
    for alias, city in CITY_ALIASES.items():
        if _normalize(alias) in normalized:
            return city
    return None


def search_vendors(
    *,
    category: str | None = None,
    city: str | None = None,
    query: str | None = None,
    limit: int = 6,
) -> list[dict]:
    vendors = load_vendors()
    normalized_query = _normalize(query) if query else ""

    def matches(vendor: dict) -> bool:
        if category and vendor["category"] != category:
            return False
        if city and _normalize(vendor["city"]) != _normalize(city):
            return False
        if not normalized_query:
            return True
        haystack = _normalize(
            " ".join(
                [
                    vendor["name"],
                    vendor.get("short_description", ""),
                    vendor["city"],
                    vendor.get("region", ""),
                    " ".join(vendor.get("tags", [])),
                    CATEGORY_BY_ID.get(vendor["category"], vendor["category"]).label
                    if vendor["category"] in CATEGORY_BY_ID
                    else vendor["category"],
                ]
            )
        )
        return normalized_query in haystack or any(
            token in haystack for token in normalized_query.split() if len(token) > 2
        )

    filtered = [vendor for vendor in vendors if matches(vendor)]
    filtered.sort(
        key=lambda vendor: (
            0 if vendor.get("featured") else 1,
            -float(vendor.get("rating", 0)),
            -int(vendor.get("review_count", 0)),
        )
    )
    return [_vendor_card(vendor) for vendor in filtered[:limit]]


def _vendor_card(vendor: dict) -> dict:
    category = CATEGORY_BY_ID.get(vendor["category"])
    return {
        "id": vendor["id"],
        "name": vendor["name"],
        "category": vendor["category"],
        "category_label": category.label if category else vendor["category"],
        "city": vendor["city"],
        "region": vendor.get("region"),
        "rating": vendor.get("rating"),
        "review_count": vendor.get("review_count"),
        "price_from": vendor.get("price_from"),
        "price_label": vendor.get("price_label"),
        "short_description": vendor.get("short_description"),
        "tags": vendor.get("tags", []),
        "capacity_min": vendor.get("capacity_min"),
        "capacity_max": vendor.get("capacity_max"),
        "featured": vendor.get("featured", False),
        "promotion": vendor.get("promotion"),
        "availability_hint": vendor.get("availability_hint"),
        "image_url": vendor.get("image_url"),
    }


def extract_state_fields(message: str, state: dict) -> dict:
    """Lightweight NLP for MVP — no LLM required."""
    text = message.strip()
    if not text:
        return state

    category = detect_category(text) or state.get("category_focus")
    city = detect_city(text) or state.get("location")

    guest_match = re.search(r"(\d{2,4})\s*(invitados|guests|personas|comensales)", _normalize(text))
    budget_match = re.search(r"(\d{3,6})\s*€|(\d{3,6})\s*euros", text, re.IGNORECASE)

    vendors_needed = list(state.get("vendors_needed", []))
    if category and category not in vendors_needed:
        vendors_needed.append(category)

    next_state = {
        **state,
        "event_request": state.get("event_request") or text,
        "location": city,
        "category_focus": category,
        "vendors_needed": vendors_needed,
    }

    if guest_match:
        next_state["guest_count"] = int(guest_match.group(1))
    if budget_match:
        next_state["budget"] = int(budget_match.group(1) or budget_match.group(2))

    search_intent = any(
        keyword in _normalize(text)
        for keyword in (
            "buscar",
            "busca",
            "muestra",
            "mostrar",
            "recomienda",
            "recomend",
            "opciones",
            "proveedores",
            "vendors",
            "shortlist",
            "lista",
        )
    )
    next_state["search_intent"] = search_intent or bool(category and city)
    return next_state


def should_search(state: dict) -> bool:
    if state.get("search_intent"):
        return bool(state.get("location") or state.get("category_focus") or state.get("vendors_needed"))
    return bool(state.get("location") and state.get("category_focus"))


def next_missing_question(state: dict) -> str | None:
    if not state.get("location"):
        return "¿En qué ciudad o zona queréis celebrar la boda?"
    if not state.get("category_focus") and not state.get("vendors_needed"):
        return "¿Qué tipo de proveedor buscáis primero: finca, banquete, fotografía, música o wedding planner?"
    if not state.get("guest_count"):
        return "¿Cuántos invitados estimáis (aprox.)?"
    return None
