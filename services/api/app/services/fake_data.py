"""
Fake data generators for pre-MVP.
Returns realistic-looking flight and vendor results without real APIs.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta


# ── Flights ──────────────────────────────────────────────────────────────────

AIRLINES = [
    {"code": "VY", "name": "Vueling", "logo": "✈"},
    {"code": "FR", "name": "Ryanair", "logo": "✈"},
    {"code": "IB", "name": "Iberia", "logo": "✈"},
    {"code": "BA", "name": "British Airways", "logo": "✈"},
    {"code": "U2", "name": "easyJet", "logo": "✈"},
    {"code": "LH", "name": "Lufthansa", "logo": "✈"},
    {"code": "AF", "name": "Air France", "logo": "✈"},
]

AIRPORT_CITIES = {
    "LHR": "London", "LGW": "London Gatwick", "STN": "London Stansted",
    "SVQ": "Seville", "MAD": "Madrid", "BCN": "Barcelona",
    "CDG": "Paris", "AMS": "Amsterdam", "FCO": "Rome",
    "DUB": "Dublin", "LIS": "Lisbon", "MXP": "Milan",
    "VLC": "Valencia", "BIO": "Bilbao", "AGP": "Malaga",
    "ORY": "Paris Orly", "BRU": "Brussels", "ZRH": "Zurich",
}


def _guess_iata(city: str) -> str:
    city_lower = city.lower()
    mapping = {
        "london": "LHR", "seville": "SVQ", "sevilla": "SVQ",
        "madrid": "MAD", "barcelona": "BCN", "paris": "CDG",
        "amsterdam": "AMS", "rome": "FCO", "dublin": "DUB",
        "lisbon": "LIS", "milan": "MXP", "valencia": "VLC",
        "malaga": "AGP", "bilbao": "BIO", "brussels": "BRU",
        "zurich": "ZRH",
    }
    for key, iata in mapping.items():
        if key in city_lower:
            return iata
    return city[:3].upper()


def search_flights(
    origin: str,
    destination: str,
    date: str | None = None,
    adults: int = 1,
    children: int = 0,
) -> list[dict]:
    """Generate fake but realistic flight options."""
    origin_iata = _guess_iata(origin) if len(origin) != 3 else origin.upper()
    dest_iata = _guess_iata(destination) if len(destination) != 3 else destination.upper()
    origin_city = AIRPORT_CITIES.get(origin_iata, origin)
    dest_city = AIRPORT_CITIES.get(dest_iata, destination)

    # Base price varies by route
    base_price = random.randint(45, 280)
    pax = adults + children

    results = []
    airlines_pool = random.sample(AIRLINES, min(4, len(AIRLINES)))

    departures = ["06:15", "08:30", "11:00", "13:45", "16:20", "18:55", "21:10"]
    durations = [90, 105, 120, 135, 150, 165, 180]

    random.shuffle(departures)

    for i, airline in enumerate(airlines_pool):
        dep_time = departures[i]
        duration_min = random.choice(durations)
        h, m = map(int, dep_time.split(":"))
        arr_min = h * 60 + m + duration_min
        arr_time = f"{arr_min // 60:02d}:{arr_min % 60:02d}"

        stops = 0 if i < 2 else random.choice([0, 1])
        price_per_pax = base_price + (i * random.randint(10, 40)) + (stops * -20)
        total_price = price_per_pax * pax

        results.append({
            "type": "flight_card",
            "airline": airline["name"],
            "airline_code": airline["code"],
            "origin": origin_iata,
            "origin_city": origin_city,
            "destination": dest_iata,
            "destination_city": dest_city,
            "departure": dep_time,
            "arrival": arr_time,
            "duration": f"{duration_min // 60}h {duration_min % 60:02d}m",
            "stops": stops,
            "stops_label": "Direct" if stops == 0 else f"{stops} stop",
            "price_per_person": price_per_pax,
            "total_price": total_price,
            "currency": "EUR",
            "cabin": "Economy",
            "seats_left": random.randint(2, 9),
        })

    results.sort(key=lambda x: x["price_per_person"])
    return results


# ── Wedding Vendors ───────────────────────────────────────────────────────────

VENUES_SEVILLE = [
    {"name": "Hacienda Benazuza", "type": "venue", "style": "Rustic / Historic", "capacity": 300, "price_from": 8000},
    {"name": "Hotel Alfonso XIII", "type": "venue", "style": "Luxury / Palace", "capacity": 200, "price_from": 15000},
    {"name": "Cortijo El Esparragal", "type": "venue", "style": "Country Estate", "capacity": 400, "price_from": 6000},
    {"name": "Real Alcázar Gardens", "type": "venue", "style": "Historic / Outdoor", "capacity": 150, "price_from": 12000},
    {"name": "Finca La Concepción", "type": "venue", "style": "Garden / Romantic", "capacity": 250, "price_from": 5500},
]

CATERING = [
    {"name": "Abades Catering", "type": "catering", "style": "Traditional Andalusian", "price_per_head": 85},
    {"name": "Restaurante Egaña Oriza", "type": "catering", "style": "Contemporary Spanish", "price_per_head": 110},
    {"name": "Grupo Cañas y Barro", "type": "catering", "style": "Classic / Formal", "price_per_head": 75},
    {"name": "El Rincón de la Triana", "type": "catering", "style": "Tapas & Modern", "price_per_head": 65},
]

PHOTOGRAPHERS = [
    {"name": "Studio Luz Dorada", "type": "photography", "style": "Documentary / Natural", "price_from": 2200},
    {"name": "Imagen Eterna", "type": "photography", "style": "Fine Art", "price_from": 3500},
    {"name": "Boda en Sevilla", "type": "photography", "style": "Classic + Video Pack", "price_from": 1800},
    {"name": "Momentos Únicos", "type": "photography", "style": "Reportage", "price_from": 2800},
]

MUSIC = [
    {"name": "Orquesta Sevilla Sound", "type": "music", "style": "Live Band / Jazz & Pop", "price_from": 2500},
    {"name": "DJ Maestro Events", "type": "music", "style": "DJ / Electronic", "price_from": 900},
    {"name": "Flamenco & Folk Duo", "type": "music", "style": "Flamenco / Traditional", "price_from": 800},
    {"name": "Cuarteto Guadalquivir", "type": "music", "style": "String Quartet / Classical", "price_from": 1200},
]


def search_vendors(
    category: str = "all",
    location: str = "Seville",
    guest_count: int = 100,
    budget: int | None = None,
) -> list[dict]:
    """Generate fake but realistic wedding vendor options."""
    results = []

    pools = {
        "venue": VENUES_SEVILLE,
        "catering": CATERING,
        "photography": PHOTOGRAPHERS,
        "music": MUSIC,
    }

    if category == "all":
        selected_pools = list(pools.values())
    else:
        cat_lower = category.lower()
        selected_pools = []
        for key, pool in pools.items():
            if key in cat_lower or cat_lower in key:
                selected_pools.append(pool)
        if not selected_pools:
            selected_pools = list(pools.values())

    for pool in selected_pools:
        for vendor in random.sample(pool, min(2, len(pool))):
            item = {**vendor, "type": "vendor_card", "vendor_type": vendor["type"],
                    "location": location, "rating": round(random.uniform(4.2, 5.0), 1),
                    "reviews": random.randint(12, 180)}
            results.append(item)

    return results
