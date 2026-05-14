"""
Wedding vendor data seeded from Bodas.net public listings (Seville, 2025).
Used for pre-MVP demo purposes only - internal use.
"""

from __future__ import annotations
import random

# ── Venues / Haciendas (Seville) ─────────────────────────────────────────────
VENUES = [
    {"name": "Hacienda Tierra Blanca", "type": "venue", "location": "Salteras, Sevilla",
     "style": "Hacienda · Jardín", "capacity": 400, "price_from": 85, "price_unit": "€/persona",
     "rating": 4.9, "reviews": 476, "bodas_award": True,
     "description": "De los más buscados en Sevilla. Más de 960 parejas lo han contratado."},
    {"name": "Hacienda Alboreá", "type": "venue", "location": "Sevilla",
     "style": "Hacienda · Finca", "capacity": 700, "price_from": 69, "price_unit": "€/persona",
     "rating": 4.9, "reviews": 312, "bodas_award": True,
     "description": "Espacio único con instalaciones acondicionadas para toda la boda."},
    {"name": "Real Venta de Antequera", "type": "venue", "location": "Sevilla ciudad",
     "style": "Histórico · Clásico", "capacity": 500, "price_from": 4000, "price_unit": "€ alquiler",
     "rating": 4.8, "reviews": 203, "bodas_award": False,
     "description": "Casi un siglo de historia. Esencia auténtica sevillana."},
    {"name": "Hacienda El Alba", "type": "venue", "location": "Santiponce, Sevilla",
     "style": "Hacienda · Catering propio", "capacity": 500, "price_from": 88, "price_unit": "€/persona",
     "rating": 4.8, "reviews": 178, "bodas_award": False,
     "description": "Gestionada por Catering Joaquín Jaén. Ubicación privilegiada cerca de Sevilla."},
    {"name": "Hacienda Caridad", "type": "venue", "location": "Alcalá de Guadaíra, Sevilla",
     "style": "Hacienda · Elegante", "capacity": 550, "price_from": 2500, "price_unit": "€ alquiler",
     "rating": 4.7, "reviews": 145, "bodas_award": False,
     "description": "Entorno elegante sin renunciar al encanto natural."},
    {"name": "Hacienda La Jara", "type": "venue", "location": "Sevilla",
     "style": "Finca · Rural", "capacity": 650, "price_from": 69, "price_unit": "€/persona",
     "rating": 4.8, "reviews": 167, "bodas_award": False,
     "description": "Gran capacidad y entorno natural espectacular."},
    {"name": "Robles Bodas Espacio", "type": "venue", "location": "Triana, Sevilla",
     "style": "Hacienda · Andaluza", "capacity": 400, "price_from": 50, "price_unit": "€/persona",
     "rating": 4.7, "reviews": 132, "bodas_award": False,
     "description": "Hacienda andaluza de columnas de mármol a 5 minutos de Triana."},
    {"name": "Cortijo El Esparragal", "type": "venue", "location": "Sevilla",
     "style": "Cortijo · Trevian Catering", "capacity": 400, "price_from": 87, "price_unit": "€/persona",
     "rating": 4.8, "reviews": 221, "bodas_award": True,
     "description": "Cortijo con catering propio de primera categoría."},
    {"name": "Hacienda Torre Doña María", "type": "venue", "location": "Sevilla",
     "style": "Hacienda · Señorial", "capacity": 400, "price_from": 95, "price_unit": "€/persona",
     "rating": 4.8, "reviews": 156, "bodas_award": False,
     "description": "Arquitectura señorial y servicio impecable."},
    {"name": "La Caprichosa", "type": "venue", "location": "Sevilla",
     "style": "Hacienda histórica · 1929", "capacity": 1000, "price_from": 1, "price_unit": "consultar",
     "rating": 4.9, "reviews": 89, "bodas_award": False,
     "description": "Diseñada por Aníbal González en 1929. Historia y elegancia incomparables."},
]

# ── Catering ──────────────────────────────────────────────────────────────────
CATERING = [
    {"name": "Matalahúva Catering", "type": "catering", "location": "Alcalá de Guadaíra, Sevilla",
     "style": "Mediterráneo · Creativo", "price_per_head": 90, "price_max": 120,
     "rating": 4.9, "reviews": 198, "bodas_award": True,
     "description": "Cocina creativa con raíces mediterráneas. 98% de parejas lo recomiendan."},
    {"name": "Medinaceli Catering", "type": "catering", "location": "Sevilla",
     "style": "Tradicional sevillano", "price_per_head": 95, "price_max": 130,
     "rating": 4.8, "reviews": 145, "bodas_award": False,
     "description": "Todo el sabor de la gastronomía andaluza para el día de vuestra boda."},
    {"name": "Pando Catering", "type": "catering", "location": "Dos Hermanas, Sevilla",
     "style": "Alta cocina · Versátil", "price_per_head": 70, "price_max": 100,
     "rating": 4.8, "reviews": 167, "bodas_award": False,
     "description": "Gastronomía de primer nivel en su exclusiva hacienda o donde elijas."},
    {"name": "Sartoria Catering Sevilla", "type": "catering", "location": "Sevilla",
     "style": "Moderno · A medida", "price_per_head": 75, "price_max": 110,
     "rating": 4.7, "reviews": 112, "bodas_award": False,
     "description": "Propuestas a medida de cada pareja."},
    {"name": "Alabardero Catering", "type": "catering", "location": "Sevilla",
     "style": "Premium · Gastronómico", "price_per_head": 100, "price_max": 150,
     "rating": 4.9, "reviews": 234, "bodas_award": True,
     "description": "La referencia gastronómica de Sevilla en eventos de alto nivel."},
    {"name": "Delirios Catering", "type": "catering", "location": "Sevilla",
     "style": "Innovador · Contemporáneo", "price_per_head": 80, "price_max": 115,
     "rating": 4.8, "reviews": 189, "bodas_award": False,
     "description": "Capacidad hasta 2000 personas. Propuestas innovadoras."},
]

# ── Photography ───────────────────────────────────────────────────────────────
PHOTOGRAPHERS = [
    {"name": "Estamosgrabando", "type": "photography", "location": "Sevilla",
     "style": "Foto + Vídeo · Reportaje", "price_from": 1600, "price_max": 3200,
     "rating": 4.9, "reviews": 284, "bodas_award": True,
     "description": "Equipo de referencia en Sevilla. Foto y vídeo con enfoque documental."},
    {"name": "Foto Stilo Azahar", "type": "photography", "location": "Sevilla capital",
     "style": "Clásico · Natural · Vídeo", "price_from": 395, "price_max": 1697,
     "rating": 4.9, "reviews": 210, "bodas_award": True,
     "description": "Más de 30 años de experiencia. 98% de recomendación."},
    {"name": "GetWild - Fotografía y vídeo", "type": "photography", "location": "Sevilla",
     "style": "Documental · Artístico", "price_from": 1390, "price_max": 2800,
     "rating": 5.0, "reviews": 17, "bodas_award": False,
     "description": "Fotografía y vídeo con mirada única y personal."},
    {"name": "Sonora Bodas", "type": "photography", "location": "Sevilla",
     "style": "Foto + Vídeo · Drone", "price_from": 1095, "price_max": 2295,
     "rating": 4.8, "reviews": 167, "bodas_award": False,
     "description": "Vídeo + foto + drone. Toque cinematográfico muy valorado."},
    {"name": "Lfstudio Sevilla", "type": "photography", "location": "Sevilla",
     "style": "Natural · Económico", "price_from": 200, "price_max": 1000,
     "rating": 4.9, "reviews": 126, "bodas_award": False,
     "description": "Muy económico, entrega rápida, adaptable a cualquier circunstancia."},
    {"name": "Lola Pérez Studio", "type": "photography", "location": "Sevilla",
     "style": "Fine Art · Premium", "price_from": 1850, "price_max": 3500,
     "rating": 5.0, "reviews": 38, "bodas_award": True,
     "description": "Fotografía de bodas de autor con un estilo artístico y elegante."},
    {"name": "Juan Luis Morilla", "type": "photography", "location": "Sevilla",
     "style": "Reportaje · Alta gama", "price_from": 2400, "price_max": 4500,
     "rating": 5.0, "reviews": 64, "bodas_award": True,
     "description": "Fotógrafo de referencia en Andalucía. Estilo editorial."},
]

# ── Music / DJ ────────────────────────────────────────────────────────────────
MUSIC = [
    {"name": "Elegancia de Fiesta", "type": "music", "location": "Sevilla",
     "style": "DJ + Sonido + Animación", "price_from": 450, "price_max": 2000,
     "rating": 4.9, "reviews": 353, "bodas_award": True,
     "description": "Sello de Oro en Bodas.net desde 2011. Wedding Awards desde 2014. 30 años de experiencia."},
    {"name": "Grupo Bumburay", "type": "music", "location": "Sevilla",
     "style": "Grupo en vivo · Versátil", "price_from": 1100, "price_max": 2500,
     "rating": 4.9, "reviews": 145, "bodas_award": True,
     "description": "Grupo en directo con amplio repertorio para ceremonia, cóctel y baile."},
    {"name": "Grupo Reyther D'Akokán", "type": "music", "location": "Sevilla",
     "style": "Salsa · Música cubana · Latino", "price_from": 1700, "price_max": 3000,
     "rating": 4.8, "reviews": 89, "bodas_award": False,
     "description": "Quinteto y sexteto en vivo. Salsa, bachata, merengue, cha-cha-chá."},
    {"name": "Spirit Music DJ's", "type": "music", "location": "Sevilla",
     "style": "DJ Premium · Animación", "price_from": 900, "price_max": 1800,
     "rating": 4.8, "reviews": 112, "bodas_award": False,
     "description": "DJ profesional con equipo de alta gama y animación personalizada."},
    {"name": "Cuarteto Isbilya", "type": "music", "location": "Sevilla",
     "style": "Cuarteto de cuerda · Clásico", "price_from": 600, "price_max": 1400,
     "rating": 4.9, "reviews": 78, "bodas_award": True,
     "description": "Cuarteto de cuerda clásico para ceremonia y cóctel. Muy recomendado."},
    {"name": "Panda Canalla", "type": "music", "location": "Sevilla",
     "style": "Banda indie · Alternativa", "price_from": 1200, "price_max": 2200,
     "rating": 4.8, "reviews": 56, "bodas_award": False,
     "description": "Banda diferente para bodas que buscan algo especial y divertido."},
]


def _guess_iata(city: str) -> str:
    mapping = {
        "london": "LHR", "seville": "SVQ", "sevilla": "SVQ",
        "madrid": "MAD", "barcelona": "BCN", "paris": "CDG",
        "amsterdam": "AMS", "rome": "FCO", "dublin": "DUB",
        "lisbon": "LIS", "milan": "MXP", "valencia": "VLC",
        "malaga": "AGP", "bilbao": "BIO", "brussels": "BRU",
        "zurich": "ZRH", "new york": "JFK", "nyc": "JFK",
        "berlin": "BER", "vienna": "VIE", "prague": "PRG",
    }
    c = city.lower()
    for key, iata in mapping.items():
        if key in c:
            return iata
    return city[:3].upper()


AIRPORTS = {
    "LHR": "London Heathrow", "LGW": "London Gatwick", "STN": "London Stansted",
    "SVQ": "Sevilla", "MAD": "Madrid", "BCN": "Barcelona",
    "CDG": "Paris CDG", "AMS": "Amsterdam", "FCO": "Rome Fiumicino",
    "DUB": "Dublin", "LIS": "Lisbon", "MXP": "Milan Malpensa",
    "VLC": "Valencia", "BIO": "Bilbao", "AGP": "Málaga",
    "BRU": "Brussels", "ZRH": "Zurich", "BER": "Berlin",
    "VIE": "Vienna", "PRG": "Prague", "JFK": "New York JFK",
}

AIRLINES = [
    ("Vueling", "VY"), ("Ryanair", "FR"), ("Iberia", "IB"),
    ("British Airways", "BA"), ("easyJet", "U2"), ("Lufthansa", "LH"),
    ("Air France", "AF"), ("KLM", "KL"), ("Volotea", "V7"),
]


def search_flights(origin: str, destination: str, date: str | None = None,
                   adults: int = 1, children: int = 0) -> list[dict]:
    origin_iata = _guess_iata(origin) if len(origin) != 3 else origin.upper()
    dest_iata = _guess_iata(destination) if len(destination) != 3 else destination.upper()
    origin_city = AIRPORTS.get(origin_iata, origin.title())
    dest_city = AIRPORTS.get(dest_iata, destination.title())

    pax = max(1, adults + children)
    base = random.randint(49, 249)
    pool = random.sample(AIRLINES, min(4, len(AIRLINES)))
    dep_times = ["06:20", "08:45", "11:10", "13:35", "16:55", "19:20", "21:40"]
    random.shuffle(dep_times)

    results = []
    for i, (airline, code) in enumerate(pool):
        dur = random.randint(85, 200)
        h, m = map(int, dep_times[i].split(":"))
        arr = f"{(h * 60 + m + dur) // 60 % 24:02d}:{(h * 60 + m + dur) % 60:02d}"
        stops = 0 if i < 2 else random.choice([0, 1])
        ppp = base + i * random.randint(8, 35) - stops * 15
        results.append({
            "type": "flight_card",
            "airline": airline, "airline_code": code,
            "origin": origin_iata, "origin_city": origin_city,
            "destination": dest_iata, "destination_city": dest_city,
            "departure": dep_times[i], "arrival": arr,
            "duration": f"{dur // 60}h {dur % 60:02d}m",
            "stops": stops, "stops_label": "Directo" if stops == 0 else f"{stops} escala",
            "price_per_person": ppp, "total_price": ppp * pax,
            "currency": "EUR", "cabin": "Economy",
            "seats_left": random.randint(2, 9),
        })
    results.sort(key=lambda x: x["price_per_person"])
    return results


def search_vendors(category: str = "all", location: str = "Seville",
                   guest_count: int = 100, budget: int | None = None) -> list[dict]:
    cat = category.lower()
    pools: list[list] = []

    if cat in ("all", "venue", "finca", "hacienda", "lugar", "espacio"):
        pools.append(VENUES)
    if cat in ("all", "catering", "banquete", "comida"):
        pools.append(CATERING)
    if cat in ("all", "photography", "foto", "fotografo", "fotografia", "video"):
        pools.append(PHOTOGRAPHERS)
    if cat in ("all", "music", "musica", "dj", "banda", "grupo"):
        pools.append(MUSIC)

    if not pools:
        pools = [VENUES, CATERING, PHOTOGRAPHERS, MUSIC]

    results = []
    for pool in pools:
        # Filter by guest capacity for venues
        filtered = pool
        if guest_count and pool is VENUES:
            filtered = [v for v in pool if v.get("capacity", 999) >= guest_count] or pool

        sample = random.sample(filtered, min(3, len(filtered)))
        for v in sample:
            item = {**v, "vendor_type": v["type"]}
            # Add price display
            if "price_per_head" in v:
                item["price_display"] = f"Desde {v['price_per_head']}€/persona"
            elif "price_from" in v and v["price_from"] > 100:
                item["price_display"] = f"Desde {v['price_from']}€"
            else:
                item["price_display"] = f"Desde {v.get('price_from', '?')}€/persona"
            if v.get("bodas_award"):
                item["badge"] = "🏆 Wedding Award"
            results.append(item)

    return results
