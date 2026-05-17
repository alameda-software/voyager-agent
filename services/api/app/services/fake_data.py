"""
Travel inventory fixtures for Voyager pre-MVP.
- Flights: generated dynamically (realistic pricing)
- Hotels: curated fixtures per city
- Car rentals: curated fixtures per city
- Wedding vendors: seeded from Bodas.net (Seville, 2025)
All used for demo/pre-MVP purposes only.
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


# ── Florists ─────────────────────────────────────────────────────────────────
FLORISTS = [
    {"name": "Flores Sevilla · La Azalea", "type": "florist", "location": "Sevilla",
     "style": "Romántico · Natural", "price_from": 800, "rating": 4.9, "reviews": 134,
     "description": "Especialistas en bodas románticas. Arreglos florales y decoración completa."},
    {"name": "Jardín Secreto Eventos", "type": "florist", "location": "Sevilla",
     "style": "Boho · Silvestre", "price_from": 600, "rating": 4.8, "reviews": 89,
     "description": "Estilo boho y silvestre. Flores de temporada y decoración de espacios."},
    {"name": "Floristería Triana", "type": "florist", "location": "Triana, Sevilla",
     "style": "Clásico · Elegante", "price_from": 500, "rating": 4.7, "reviews": 67,
     "description": "Más de 20 años en el sector. Clásico andaluz con toque de elegancia."},
    {"name": "La Espiga Dorada", "type": "florist", "location": "Sevilla",
     "style": "Moderno · Minimalista", "price_from": 900, "rating": 4.9, "reviews": 112,
     "description": "Diseño floral minimalista y contemporáneo. Premio mejor floristería 2024."},
]

# ── Wedding Cakes ─────────────────────────────────────────────────────────────
CAKES = [
    {"name": "Dulce Evento · Pastelería Nupcial", "type": "cake", "location": "Sevilla",
     "style": "Artístico · A medida", "price_from": 350, "rating": 5.0, "reviews": 203,
     "description": "Tartas nupciales de diseño único. Degustación gratuita incluida."},
    {"name": "La Tarta de Ana", "type": "cake", "location": "Sevilla",
     "style": "Fondant · Clásico", "price_from": 250, "rating": 4.9, "reviews": 178,
     "description": "Especialistas en fondant y decoración artesanal. Más de 500 bodas."},
    {"name": "Sugar & Dreams", "type": "cake", "location": "Sevilla",
     "style": "Naked cake · Boho", "price_from": 280, "rating": 4.8, "reviews": 145,
     "description": "Naked cakes y semi-naked con flores naturales. Muy instagrameable."},
    {"name": "Pastelería Alfonso", "type": "cake", "location": "Sevilla",
     "style": "Tradicional · Sabores únicos", "price_from": 200, "rating": 4.7, "reviews": 89,
     "description": "Tradición sevillana desde 1978. Sabores únicos y precios accesibles."},
]

# ── Transport ─────────────────────────────────────────────────────────────────
TRANSPORT = [
    {"name": "Bodas en Rolls Royce Sevilla", "type": "transport", "location": "Sevilla",
     "style": "Rolls Royce · Lujo", "price_from": 450, "rating": 5.0, "reviews": 89,
     "description": "Rolls Royce Silver Shadow y Phantom. El toque de lujo para tu gran día."},
    {"name": "Coche de Época Sevilla", "type": "transport", "location": "Sevilla",
     "style": "Vintage · Época", "price_from": 300, "rating": 4.9, "reviews": 134,
     "description": "Jaguar, Citroën DS, Mercedes clásico. Fotos espectaculares garantizadas."},
    {"name": "Limusinas & Eventos SVQ", "type": "transport", "location": "Sevilla",
     "style": "Limusina · Grupo", "price_from": 350, "rating": 4.7, "reviews": 67,
     "description": "Limusinas para novia y grupo. Servicio de chófer y decoración incluida."},
    {"name": "Autocares Boda Sevilla", "type": "transport", "location": "Sevilla",
     "style": "Autobús invitados", "price_from": 280, "rating": 4.6, "reviews": 45,
     "description": "Traslado de invitados en autobús. Puntual y con conductor de librea."},
]

# ── Makeup & Beauty ───────────────────────────────────────────────────────────
BEAUTY = [
    {"name": "Maquillaje Nupcial · Rocío García", "type": "beauty", "location": "Sevilla",
     "style": "Natural · Airbrush", "price_from": 250, "rating": 5.0, "reviews": 312,
     "description": "Maquillaje airbrush de larga duración. Prueba incluida. 500+ novias."},
    {"name": "Estudio Novia Sevilla", "type": "beauty", "location": "Sevilla",
     "style": "Makeup + Peluquería", "price_from": 350, "rating": 4.9, "reviews": 234,
     "description": "Pack completo makeup + peinado. Para novia y séquito."},
    {"name": "Glamour & Arte Nupcial", "type": "beauty", "location": "Sevilla",
     "style": "Glam · Editorial", "price_from": 300, "rating": 4.8, "reviews": 167,
     "description": "Estilo editorial y glamuroso. Especialistas en novias morenas."},
]

# ── Invitations & Stationery ──────────────────────────────────────────────────
INVITATIONS = [
    {"name": "Papel & Tinta Bodas", "type": "invitations", "location": "Sevilla",
     "style": "Artesanal · Letterpress", "price_from": 180, "rating": 4.9, "reviews": 145,
     "description": "Invitaciones letterpress artesanales. Diseño personalizado incluido."},
    {"name": "Invitaciones Únicas SVQ", "type": "invitations", "location": "Sevilla",
     "style": "Moderno · Minimalista", "price_from": 120, "rating": 4.8, "reviews": 89,
     "description": "Diseños modernos y minimalistas. Entrega en 10 días laborables."},
    {"name": "Detallería Nupcial", "type": "invitations", "location": "Sevilla",
     "style": "Detalles + Invitaciones", "price_from": 200, "rating": 4.9, "reviews": 112,
     "description": "Pack invitaciones + detalles para invitados. Diseño cohesionado."},
]

# ── Wedding Planners ──────────────────────────────────────────────────────────
PLANNERS = [
    {"name": "Bodas con Alma · Sevilla", "type": "planner", "location": "Sevilla",
     "style": "Full planning · Coordinación", "price_from": 2500, "rating": 5.0, "reviews": 89,
     "description": "Wedding planner full service. Desde el primer día hasta el gran día."},
    {"name": "Eventos & Sueños", "type": "planner", "location": "Sevilla",
     "style": "Day coordination", "price_from": 800, "rating": 4.9, "reviews": 134,
     "description": "Coordinación del día de la boda. Para que disfrutéis sin preocupaciones."},
    {"name": "The Wedding Studio Sevilla", "type": "planner", "location": "Sevilla",
     "style": "Luxury · Destination weddings", "price_from": 3500, "rating": 4.9, "reviews": 67,
     "description": "Especialistas en bodas de lujo y destination weddings en Andalucía."},
]

VENDOR_POOLS = {
    "venue": VENUES,
    "catering": CATERING,
    "photography": PHOTOGRAPHERS,
    "music": MUSIC,
    "florist": FLORISTS,
    "cake": CAKES,
    "transport": TRANSPORT,
    "beauty": BEAUTY,
    "invitations": INVITATIONS,
    "planner": PLANNERS,
}

VENDOR_ALIASES = {
    "finca": "venue", "hacienda": "venue", "lugar": "venue", "espacio": "venue", "salon": "venue",
    "banquete": "catering", "comida": "catering",
    "foto": "photography", "fotografo": "photography", "fotografia": "photography", "video": "photography",
    "dj": "music", "banda": "music", "grupo": "music", "musica": "music",
    "flores": "florist", "florista": "florist", "decoracion": "florist",
    "tarta": "cake", "pastel": "cake", "cake": "cake",
    "coche": "transport", "autobus": "transport", "limusina": "transport", "transporte": "transport",
    "maquillaje": "beauty", "peluqueria": "beauty", "belleza": "beauty", "makeup": "beauty",
    "invitaciones": "invitations", "papeleria": "invitations", "detalles": "invitations",
    "wedding planner": "planner", "organizador": "planner", "coordinador": "planner",
}


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


# ── Hotels ───────────────────────────────────────────────────────────────────
HOTELS = {
    "default": [
        {"name": "Hotel Alfonso XIII", "chain": "Luxury Collection", "stars": 5,
         "location": "Centro, Sevilla", "price_per_night": 420, "rating": 9.2,
         "reviews": 3841, "amenities": ["Pool", "Spa", "Bar", "Restaurant", "Parking"],
         "description": "Palacio histórico de 1928. El hotel más icónico de Sevilla."},
        {"name": "Hotel Mercer Sevilla", "chain": "Mercer Hotels", "stars": 5,
         "location": "Santa Cruz, Sevilla", "price_per_night": 380, "rating": 9.4,
         "reviews": 1203, "amenities": ["Rooftop Pool", "Spa", "Restaurant", "Gym"],
         "description": "Palacio del s. XVI en el corazón de Santa Cruz."},
        {"name": "EME Catedral Hotel", "chain": "Independent", "stars": 5,
         "location": "Catedral, Sevilla", "price_per_night": 295, "rating": 9.0,
         "reviews": 2567, "amenities": ["Rooftop Pool", "Bar", "Restaurant", "Terrace"],
         "description": "Vistas directas a la Giralda. Rooftop bar espectacular."},
        {"name": "Hotel Hospes Las Casas del Rey de Baeza", "chain": "Hospes", "stars": 4,
         "location": "Santa Cruz, Sevilla", "price_per_night": 185, "rating": 9.1,
         "reviews": 1876, "amenities": ["Pool", "Restaurant", "Bar", "Terrace"],
         "description": "Casa señorial del s. XVIII. Patio andaluz incomparable."},
        {"name": "Hotel Boutique Doña Lina", "chain": "Independent", "stars": 4,
         "location": "Centro, Sevilla", "price_per_night": 145, "rating": 8.9,
         "reviews": 987, "amenities": ["Pool", "Bar", "Terrace", "Free WiFi"],
         "description": "Hotel boutique con patio sevillano y encanto personal."},
    ],
    "london": [
        {"name": "The Savoy", "chain": "Fairmont", "stars": 5,
         "location": "Strand, London", "price_per_night": 650, "rating": 9.3,
         "reviews": 5621, "amenities": ["Spa", "Pool", "Restaurant", "Bar", "Gym"],
         "description": "El hotel más icónico de Londres desde 1889."},
        {"name": "Shangri-La The Shard", "chain": "Shangri-La", "stars": 5,
         "location": "London Bridge, London", "price_per_night": 490, "rating": 9.1,
         "reviews": 3241, "amenities": ["Pool", "Spa", "Restaurant", "Sky Bar", "Gym"],
         "description": "Vistas panorámicas de Londres desde el icónico The Shard."},
        {"name": "citizenM Tower of London", "chain": "citizenM", "stars": 4,
         "location": "Tower Hill, London", "price_per_night": 165, "rating": 8.8,
         "reviews": 8934, "amenities": ["Bar", "Free WiFi", "Gym", "24h Reception"],
         "description": "Diseño moderno, precio inteligente, ubicación perfecta."},
        {"name": "Premier Inn London City", "chain": "Premier Inn", "stars": 3,
         "location": "City of London", "price_per_night": 119, "rating": 8.4,
         "reviews": 12043, "amenities": ["Restaurant", "Bar", "Free WiFi"],
         "description": "Calidad garantizada Premier Inn en pleno corazón financiero."},
        {"name": "Point A Hotel London Kings Cross", "chain": "Point A", "stars": 3,
         "location": "Kings Cross, London", "price_per_night": 89, "rating": 8.2,
         "reviews": 6712, "amenities": ["Free WiFi", "24h Reception", "Bar"],
         "description": "Compacto, eficiente y bien conectado. Ideal para city breaks."},
    ],
    "paris": [
        {"name": "Le Meurice", "chain": "Dorchester Collection", "stars": 5,
         "location": "1er arrondissement, Paris", "price_per_night": 890, "rating": 9.5,
         "reviews": 2341, "amenities": ["Spa", "Restaurant", "Bar", "Concierge"],
         "description": "El hotel de los reyes. Frente a las Tullerías."},
        {"name": "Hotel des Grands Boulevards", "chain": "Independent", "stars": 4,
         "location": "2e arrondissement, Paris", "price_per_night": 245, "rating": 9.0,
         "reviews": 1876, "amenities": ["Restaurant", "Bar", "Terrace", "Free WiFi"],
         "description": "Boutique hotel con restaurante de culto en los Grandes Bulevares."},
        {"name": "Generator Paris", "chain": "Generator", "stars": 3,
         "location": "10e arrondissement, Paris", "price_per_night": 75, "rating": 8.3,
         "reviews": 9823, "amenities": ["Bar", "Free WiFi", "Restaurant", "Lounge"],
         "description": "Diseño urbano, ambiente social, precio imbatible en París."},
    ],
    "madrid": [
        {"name": "Hotel Ritz Madrid", "chain": "Mandarin Oriental", "stars": 5,
         "location": "Paseo del Prado, Madrid", "price_per_night": 580, "rating": 9.4,
         "reviews": 3241, "amenities": ["Spa", "Pool", "Restaurant", "Bar", "Gym"],
         "description": "El gran hotel de Madrid desde 1910. Restaurado con exquisitez."},
        {"name": "Vincci The Mint", "chain": "Vincci", "stars": 4,
         "location": "Gran Vía, Madrid", "price_per_night": 175, "rating": 8.9,
         "reviews": 2109, "amenities": ["Rooftop Bar", "Restaurant", "Free WiFi", "Gym"],
         "description": "Hotel de diseño en la Gran Vía con rooftop con vistas."},
        {"name": "Room Mate Oscar", "chain": "Room Mate", "stars": 4,
         "location": "Chueca, Madrid", "price_per_night": 135, "rating": 8.7,
         "reviews": 3876, "amenities": ["Rooftop Pool", "Bar", "Free WiFi"],
         "description": "Hotel boutique vibrante en el barrio más animado de Madrid."},
    ],
}

# ── Car Rentals ───────────────────────────────────────────────────────────────
CAR_RENTALS = [
    {"company": "Europcar", "logo_hint": "🟢",
     "cars": [
         {"category": "Economy", "model": "VW Polo o similar", "doors": 5,
          "seats": 5, "transmission": "Manual", "ac": True,
          "price_per_day": 28, "price_total_hint": True,
          "included": ["Seguro básico", "Kilometraje ilimitado"],
          "extras": ["GPS +5€/día", "Conductor adicional +8€/día"]},
         {"category": "Compact", "model": "VW Golf o similar", "doors": 5,
          "seats": 5, "transmission": "Manual", "ac": True,
          "price_per_day": 42, "price_total_hint": True,
          "included": ["Seguro completo", "Kilometraje ilimitado"],
          "extras": ["GPS +5€/día", "Silla bebé +8€/día"]},
         {"category": "SUV", "model": "Seat Ateca o similar", "doors": 5,
          "seats": 5, "transmission": "Automático", "ac": True,
          "price_per_day": 68, "price_total_hint": True,
          "included": ["Seguro completo", "Kilometraje ilimitado"],
          "extras": ["GPS +5€/día"]},
     ]},
    {"company": "Hertz", "logo_hint": "🟡",
     "cars": [
         {"category": "Economy", "model": "Fiat 500 o similar", "doors": 3,
          "seats": 4, "transmission": "Manual", "ac": True,
          "price_per_day": 32, "price_total_hint": True,
          "included": ["Seguro básico", "250km/día"],
          "extras": ["Km ilimitado +6€/día", "GPS +6€/día"]},
         {"category": "Compact", "model": "Toyota Corolla o similar", "doors": 4,
          "seats": 5, "transmission": "Automático", "ac": True,
          "price_per_day": 55, "price_total_hint": True,
          "included": ["Seguro completo", "Kilometraje ilimitado"],
          "extras": ["GPS +6€/día", "Conductor joven +10€/día"]},
     ]},
    {"company": "Sixt", "logo_hint": "🟠",
     "cars": [
         {"category": "Economy", "model": "Opel Corsa o similar", "doors": 5,
          "seats": 5, "transmission": "Manual", "ac": True,
          "price_per_day": 29, "price_total_hint": True,
          "included": ["Seguro básico", "Kilometraje ilimitado"],
          "extras": ["GPS +4€/día", "Seguro premium +12€/día"]},
         {"category": "Premium", "model": "BMW Serie 3 o similar", "doors": 4,
          "seats": 5, "transmission": "Automático", "ac": True,
          "price_per_day": 95, "price_total_hint": True,
          "included": ["Seguro completo", "Kilometraje ilimitado"],
          "extras": ["GPS incluido", "Conductor adicional +8€/día"]},
     ]},
    {"company": "Avis", "logo_hint": "🔴",
     "cars": [
         {"category": "Economy", "model": "Renault Clio o similar", "doors": 5,
          "seats": 5, "transmission": "Manual", "ac": True,
          "price_per_day": 31, "price_total_hint": True,
          "included": ["Seguro básico", "Kilometraje ilimitado"],
          "extras": ["GPS +5€/día", "Seguro total +15€/día"]},
         {"category": "Family", "model": "Peugeot 3008 o similar", "doors": 5,
          "seats": 7, "transmission": "Automático", "ac": True,
          "price_per_day": 72, "price_total_hint": True,
          "included": ["Seguro completo", "Kilometraje ilimitado"],
          "extras": ["Silla bebé +7€/día", "GPS +5€/día"]},
     ]},
]


def search_hotels(destination: str, checkin: str | None = None, checkout: str | None = None,
                 adults: int = 1, children: int = 0, nights: int = 3) -> list[dict]:
    """Return hotel options for a destination."""
    dest_lower = destination.lower()
    city_key = "default"
    for key in HOTELS:
        if key in dest_lower:
            city_key = key
            break
    # Also match by airport code
    if city_key == "default":
        iata = _guess_iata(destination)
        if iata == "LHR" or iata == "LGW" or iata == "STN":
            city_key = "london"
        elif iata == "CDG" or iata == "ORY":
            city_key = "paris"
        elif iata == "MAD":
            city_key = "madrid"

    pool = HOTELS.get(city_key, HOTELS["default"])
    results = []
    for h in random.sample(pool, min(4, len(pool))):
        total = h["price_per_night"] * max(1, nights)
        results.append({
            "type": "hotel_card",
            **h,
            "nights": nights,
            "total_price": total,
            "currency": "EUR",
            "checkin": checkin or "Flexible",
            "checkout": checkout or "Flexible",
        })
    results.sort(key=lambda x: x["price_per_night"])
    return results


def search_car_rentals(location: str, pickup_date: str | None = None,
                       dropoff_date: str | None = None, days: int = 3,
                       category: str | None = None) -> list[dict]:
    """Return car rental options."""
    results = []
    cat_lower = (category or "").lower()
    for company in CAR_RENTALS:
        for car in company["cars"]:
            if cat_lower and cat_lower not in car["category"].lower():
                continue
            total = car["price_per_day"] * max(1, days)
            results.append({
                "type": "car_card",
                "company": company["company"],
                "logo_hint": company["logo_hint"],
                **car,
                "days": days,
                "total_price": total,
                "currency": "EUR",
                "pickup_location": location,
                "pickup_date": pickup_date or "Flexible",
                "dropoff_date": dropoff_date or "Flexible",
            })
    results.sort(key=lambda x: x["price_per_day"])
    return results[:8]


def search_vendors(category: str = "all", location: str = "Seville",
                   guest_count: int = 100, budget: int | None = None) -> list[dict]:
    cat = category.lower().strip()
    # Resolve alias
    resolved = VENDOR_ALIASES.get(cat, cat)

    if resolved == "all" or cat == "all":
        # Return 2 from each main category
        selected_pools = [(k, v) for k, v in VENDOR_POOLS.items()]
    else:
        pool = VENDOR_POOLS.get(resolved)
        if pool:
            selected_pools = [(resolved, pool)]
        else:
            # Fuzzy match
            selected_pools = [(k, v) for k, v in VENDOR_POOLS.items() if resolved in k or k in resolved]
        if not selected_pools:
            selected_pools = [(k, v) for k, v in VENDOR_POOLS.items()]

    results = []
    for pool_name, pool in selected_pools:
        filtered = pool
        if guest_count and pool_name == "venue":
            filtered = [v for v in pool if v.get("capacity", 999) >= guest_count] or pool

        n = 3 if len(selected_pools) == 1 else 2
        sample = random.sample(filtered, min(n, len(filtered)))
        for v in sample:
            item = {**v, "vendor_type": v["type"]}
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
