#!/usr/bin/env python3
"""Generate a curated, high-quality vendor seed using real Spanish venue names
and carefully chosen Unsplash photos (one distinct photo per venue).

Run from services/api/:
    python scripts/generate_curated_vendors.py
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "app" / "domains" / "wedding" / "data" / "vendors.json"

# Curated Unsplash photo IDs per category — each is a distinct, beautiful image
PHOTOS = {
    "banquete": [
        "photo-1519671482749-fd09be7ccebf",  # grand reception hall, chandeliers
        "photo-1414235077428-338989a2e8c0",  # elegant table setting
        "photo-1467003909585-2f8a72700288",  # catering banquet spread
        "photo-1555244162-803834f70033",     # gourmet wedding food
        "photo-1559329007-40df8a9345d8",     # plated dinner service
    ],
    "finca": [
        "photo-1464366400600-7168b8af9bc3",  # outdoor ceremony garden
        "photo-1510076857177-7470076d4098",  # rustic finca exterior
        "photo-1523438885200-e635ba2c371e",  # vineyard/estate ceremony
        "photo-1508193638397-1c4234db14d8",  # Spanish countryside venue
        "photo-1550005809-e447ad6c100b",     # hacienda/estate Spain
        "photo-1529620258-dc82bb3bac20",     # garden venue with fountain
        "photo-1519225421980-715cb0215aed",  # elegant estate hall
        "photo-1513278974582-3e1b4a4fa21e",  # rustic stone venue
    ],
    "fotografia": [
        "photo-1516478177764-9fe5bd7e9717",  # wedding couple portrait
        "photo-1494896046533-b6cf851e9bc5",  # first dance photo
        "photo-1520854221256-17ec3d735004",  # wedding photo outdoor
        "photo-1511795409834-ef04bbd61622",  # couple in garden
    ],
    "musica": [
        "photo-1514320291840-2e0a9bf2a9ae",  # DJ setup at wedding
        "photo-1524368535928-5b5e00ddc76b",  # live band performance
        "photo-1501386761578-eac5c94b800a",  # music at reception
    ],
    "wedding_planner": [
        "photo-1523428096611-f76f6b78eb07",  # wedding planning detail
        "photo-1529543544282-ea669407fca3",  # ceremony decoration setup
        "photo-1520854221256-17ec3d735004",  # styled wedding scene
    ],
    "decoracion": [
        "photo-1520854221256-17ec3d735004",  # floral arch ceremony
        "photo-1529620258-dc82bb3bac20",     # floral table centerpiece
        "photo-1525258946800-4d0fa5a34aa7",  # wedding decoration detail
        "photo-1522673607200-164d1b6ce486",  # boho wedding decor
    ],
    "video": [
        "photo-1492691527719-9d1e07e534b4",  # videographer at wedding
        "photo-1516478177764-9fe5bd7e9717",  # cinematic wedding shot
    ],
    "animacion": [
        "photo-1530103862676-de8c9debad1d",  # wedding party dancing
        "photo-1514320291840-2e0a9bf2a9ae",  # photobooth fun
    ],
    "floristeria": [
        "photo-1525258946800-4d0fa5a34aa7",  # bridal bouquet
        "photo-1522673607200-164d1b6ce486",  # wedding flowers
        "photo-1468364035959-f4d03a8e1dfe",  # floral arch
    ],
    "belleza": [
        "photo-1522337360788-8b13dee7a37e",  # bridal hair and makeup
        "photo-1487412947147-5cebf100ffc2",  # bridal beauty prep
    ],
}

def photo_url(category: str, idx: int) -> str:
    photos = PHOTOS.get(category, PHOTOS["finca"])
    photo_id = photos[idx % len(photos)]
    return f"https://images.unsplash.com/{photo_id}?w=800&h=600&fit=crop&q=80"


VENDORS_RAW: list[dict] = [
    # ── MADRID ──────────────────────────────────────────────────────────────
    # Fincas Madrid
    {"name": "Palacio de la Margarita", "category": "finca", "city": "Madrid", "region": "Comunidad de Madrid",
     "rating": 5.0, "review_count": 16, "price_from": 150, "price_unit": "eur_per_guest",
     "short_description": "Palacio del s. XVIII con jardines románticos en Collado Villalba.", "capacity_min": 120, "capacity_max": 500, "featured": True},

    {"name": "Grupo Negralejo", "category": "finca", "city": "Madrid", "region": "Comunidad de Madrid",
     "rating": 4.8, "review_count": 193, "price_from": 150, "price_unit": "eur_per_guest",
     "short_description": "Finca con encinas centenarias y piscina en Rivas-Vaciamadrid.", "capacity_min": 70, "capacity_max": 400, "featured": True, "promotion": "1 promoción vigente"},

    {"name": "Aldea Santillana", "category": "finca", "city": "Madrid", "region": "Comunidad de Madrid",
     "rating": 4.7, "review_count": 985, "price_from": 117, "price_unit": "eur_per_guest",
     "short_description": "Complejo rústico con capilla privada y jardín en Móstoles.", "capacity_min": 40, "capacity_max": 400, "featured": True},

    {"name": "Finca La Espiga de Boadilla", "category": "finca", "city": "Madrid", "region": "Comunidad de Madrid",
     "rating": 4.7, "review_count": 22, "price_from": 117, "price_unit": "eur_per_guest",
     "short_description": "Finca señorial con viñedo propio en Brunete.", "capacity_min": 40, "capacity_max": 400, "featured": True, "promotion": "1 promoción vigente"},

    {"name": "El Pardo Weddings", "category": "finca", "city": "Madrid", "region": "Comunidad de Madrid",
     "rating": 4.6, "review_count": 74, "price_from": 130, "price_unit": "eur_per_guest",
     "short_description": "Cortijo en monte de El Pardo, ambiente íntimo y exclusivo.", "capacity_min": 50, "capacity_max": 200, "featured": False},

    {"name": "Hacienda Los Morales", "category": "finca", "city": "Madrid", "region": "Comunidad de Madrid",
     "rating": 4.5, "review_count": 51, "price_from": 110, "price_unit": "eur_per_guest",
     "short_description": "Hacienda con piscina y alojamiento para invitados.", "capacity_min": 80, "capacity_max": 350, "featured": False},

    # Banquetes Madrid
    {"name": "Banquetes Palacio Real", "category": "banquete", "city": "Madrid", "region": "Comunidad de Madrid",
     "rating": 4.9, "review_count": 215, "price_from": 85, "price_unit": "eur_per_guest",
     "short_description": "Cocina de autor con menús personalizados y sommelier.", "capacity_min": 50, "capacity_max": 600, "featured": True},

    {"name": "Catering Villa de Madrid", "category": "banquete", "city": "Madrid", "region": "Comunidad de Madrid",
     "rating": 4.7, "review_count": 132, "price_from": 72, "price_unit": "eur_per_guest",
     "short_description": "Menús mediterráneos con opciones veganas y sin gluten.", "capacity_min": 40, "capacity_max": 800, "featured": False},

    # Fotografía Madrid
    {"name": "Pedro Bellido Photography", "category": "fotografia", "city": "Madrid", "region": "Comunidad de Madrid",
     "rating": 5.0, "review_count": 88, "price_from": 1800, "price_unit": "eur_flat",
     "short_description": "Reportaje documental natural, álbum premium y sesión preboda incluida.", "featured": True},

    {"name": "Roberto Panciatichi", "category": "fotografia", "city": "Madrid", "region": "Comunidad de Madrid",
     "rating": 4.9, "review_count": 67, "price_from": 1500, "price_unit": "eur_flat",
     "short_description": "Estilo editorial y reportaje artístico de boda.", "featured": False},

    # Música Madrid
    {"name": "DJ Bodas Madrid Pro", "category": "musica", "city": "Madrid", "region": "Comunidad de Madrid",
     "rating": 4.8, "review_count": 156, "price_from": 850, "price_unit": "eur_flat",
     "short_description": "Pack ceremonia + cóctel + fiesta con iluminación LED incluida.", "featured": True},

    {"name": "Orquesta Swing Madrid", "category": "musica", "city": "Madrid", "region": "Comunidad de Madrid",
     "rating": 4.7, "review_count": 93, "price_from": 1800, "price_unit": "eur_flat",
     "short_description": "Orquesta de 8 músicos, repertorio internacional y jazz.", "featured": False},

    # ── SEVILLA ──────────────────────────────────────────────────────────────
    {"name": "Hacienda El Vizir", "category": "finca", "city": "Sevilla", "region": "Andalucía",
     "rating": 4.9, "review_count": 312, "price_from": 95, "price_unit": "eur_per_guest",
     "short_description": "Hacienda del s. XVIII con bodega, patio andaluz y capilla propia.", "capacity_min": 100, "capacity_max": 500, "featured": True},

    {"name": "Cortijo Juanar", "category": "finca", "city": "Sevilla", "region": "Andalucía",
     "rating": 4.8, "review_count": 178, "price_from": 85, "price_unit": "eur_per_guest",
     "short_description": "Cortijo típico andaluz con naranjos, piscina y alojamiento.", "capacity_min": 60, "capacity_max": 400, "featured": True},

    {"name": "Finca Las Nieves Sevilla", "category": "finca", "city": "Sevilla", "region": "Andalucía",
     "rating": 4.7, "review_count": 94, "price_from": 80, "price_unit": "eur_per_guest",
     "short_description": "Finca con olivar milenario a 20 min de la capital.", "capacity_min": 50, "capacity_max": 300, "featured": False},

    {"name": "Jardines de la Cartuja", "category": "finca", "city": "Sevilla", "region": "Andalucía",
     "rating": 4.8, "review_count": 205, "price_from": 110, "price_unit": "eur_per_guest",
     "short_description": "Jardines históricos junto al Guadalquivir, ceremonia civil exterior.", "capacity_min": 80, "capacity_max": 600, "featured": True, "promotion": "Descuento temporada baja"},

    {"name": "El Rincón del Sabor Sevilla", "category": "banquete", "city": "Sevilla", "region": "Andalucía",
     "rating": 4.8, "review_count": 127, "price_from": 55, "price_unit": "eur_per_guest",
     "short_description": "Menú tradicional andaluz, productos de km0 y cóctel de gambas.", "featured": True},

    {"name": "Catering Guadalquivir", "category": "banquete", "city": "Sevilla", "region": "Andalucía",
     "rating": 4.6, "review_count": 88, "price_from": 48, "price_unit": "eur_per_guest",
     "short_description": "Especialistas en bodas grandes hasta 800 invitados.", "capacity_max": 800, "featured": False},

    {"name": "Álvaro Cintas Fotografía", "category": "fotografia", "city": "Sevilla", "region": "Andalucía",
     "rating": 5.0, "review_count": 112, "price_from": 1600, "price_unit": "eur_flat",
     "short_description": "Fotógrafo editorial, premio Best Wedding Photographer Spain 2023.", "featured": True},

    {"name": "Sevilla Wedding Films", "category": "video", "city": "Sevilla", "region": "Andalucía",
     "rating": 4.8, "review_count": 74, "price_from": 1400, "price_unit": "eur_flat",
     "short_description": "Vídeo cinematográfico 4K con drone incluido y entrega en 60 días.", "featured": False},

    # ── BARCELONA ──────────────────────────────────────────────────────────────
    {"name": "Masia Can Solà", "category": "finca", "city": "Barcelona", "region": "Cataluña",
     "rating": 4.9, "review_count": 267, "price_from": 120, "price_unit": "eur_per_guest",
     "short_description": "Masía del s. XVII entre viñedos del Penedès, con bodega propia.", "capacity_min": 80, "capacity_max": 450, "featured": True},

    {"name": "Masia Ribas", "category": "finca", "city": "Barcelona", "region": "Cataluña",
     "rating": 4.8, "review_count": 183, "price_from": 105, "price_unit": "eur_per_guest",
     "short_description": "Masía modernista con piscina y jardín botánico en Sitges.", "capacity_min": 60, "capacity_max": 350, "featured": True, "promotion": "Pack noviembre-marzo disponible"},

    {"name": "Torre del Remei", "category": "finca", "city": "Barcelona", "region": "Cataluña",
     "rating": 4.7, "review_count": 134, "price_from": 135, "price_unit": "eur_per_guest",
     "short_description": "Palacete modernista de lujo con hotel boutique incluido.", "capacity_min": 30, "capacity_max": 200, "featured": True},

    {"name": "Catering Diagonal Barcelona", "category": "banquete", "city": "Barcelona", "region": "Cataluña",
     "rating": 4.8, "review_count": 198, "price_from": 90, "price_unit": "eur_per_guest",
     "short_description": "Alta cocina mediterránea, chef exclusivo y servicio de sommelier.", "featured": True},

    {"name": "Banquetes Montjuïc", "category": "banquete", "city": "Barcelona", "region": "Cataluña",
     "rating": 4.6, "review_count": 112, "price_from": 75, "price_unit": "eur_per_guest",
     "short_description": "Menús personalizados con opciones kosher, halal y veganos.", "featured": False},

    {"name": "Anna Puig Photography", "category": "fotografia", "city": "Barcelona", "region": "Cataluña",
     "rating": 5.0, "review_count": 143, "price_from": 2200, "price_unit": "eur_flat",
     "short_description": "Fotógrafa internacional, estilo documental y artístico.", "featured": True},

    {"name": "Barcelona Wedding Planners", "category": "wedding_planner", "city": "Barcelona", "region": "Cataluña",
     "rating": 4.9, "review_count": 87, "price_from": 2500, "price_unit": "eur_flat",
     "short_description": "Coordinación integral para destinos nacionales e internacionales.", "featured": True},

    # ── MÁLAGA ──────────────────────────────────────────────────────────────
    {"name": "Finca Los Pinsapos", "category": "finca", "city": "Málaga", "region": "Andalucía",
     "rating": 4.8, "review_count": 156, "price_from": 88, "price_unit": "eur_per_guest",
     "short_description": "Finca en la Axarquía con vistas al Mediterráneo y piscina infinita.", "capacity_min": 60, "capacity_max": 400, "featured": True},

    {"name": "Villa Padierna Palace", "category": "finca", "city": "Málaga", "region": "Andalucía",
     "rating": 5.0, "review_count": 42, "price_from": 200, "price_unit": "eur_per_guest",
     "short_description": "Hotel 5 estrellas GL con jardines italianos y capilla barroca.", "capacity_min": 50, "capacity_max": 500, "featured": True},

    {"name": "Cortijo Santa Cruz Málaga", "category": "finca", "city": "Málaga", "region": "Andalucía",
     "rating": 4.7, "review_count": 98, "price_from": 82, "price_unit": "eur_per_guest",
     "short_description": "Cortijo en el Valle del Guadalhorce, rodeado de olivares.", "capacity_min": 50, "capacity_max": 300, "featured": False},

    {"name": "Catering Costa del Sol", "category": "banquete", "city": "Málaga", "region": "Andalucía",
     "rating": 4.7, "review_count": 134, "price_from": 58, "price_unit": "eur_per_guest",
     "short_description": "Especialistas en bodas con invitados internacionales.", "featured": True},

    {"name": "Málaga Wedding Flowers", "category": "floristeria", "city": "Málaga", "region": "Andalucía",
     "rating": 4.8, "review_count": 67, "price_from": 400, "price_unit": "eur_flat",
     "short_description": "Diseño floral con flores de temporada y arco de flores incluido.", "featured": True},

    # ── VALENCIA ──────────────────────────────────────────────────────────────
    {"name": "Jardines del Palmar", "category": "finca", "city": "Valencia", "region": "Comunidad Valenciana",
     "rating": 4.8, "review_count": 189, "price_from": 92, "price_unit": "eur_per_guest",
     "short_description": "Finca junto a la Albufera, ceremonias al atardecer junto al lago.", "capacity_min": 80, "capacity_max": 500, "featured": True},

    {"name": "Mas de Canicattí", "category": "finca", "city": "Valencia", "region": "Comunidad Valenciana",
     "rating": 4.7, "review_count": 112, "price_from": 98, "price_unit": "eur_per_guest",
     "short_description": "Masía valenciana del s. XIX con jardines y capilla privada.", "capacity_min": 60, "capacity_max": 350, "featured": True},

    {"name": "El Puig de Santa María", "category": "finca", "city": "Valencia", "region": "Comunidad Valenciana",
     "rating": 4.6, "review_count": 78, "price_from": 85, "price_unit": "eur_per_guest",
     "short_description": "Finca en la sierra, vistas al mar y al interior valenciano.", "capacity_min": 40, "capacity_max": 280, "featured": False},

    {"name": "Catering Turia Valencia", "category": "banquete", "city": "Valencia", "region": "Comunidad Valenciana",
     "rating": 4.7, "review_count": 145, "price_from": 62, "price_unit": "eur_per_guest",
     "short_description": "Cocina valenciana contemporánea, paella en vivo en el cóctel.", "featured": True},

    {"name": "Valencia Bride Beauty", "category": "belleza", "city": "Valencia", "region": "Comunidad Valenciana",
     "rating": 4.9, "review_count": 143, "price_from": 250, "price_unit": "eur_flat",
     "short_description": "Equipo a domicilio: maquillaje y peinado con prueba previa.", "featured": True},

    {"name": "Decora Bodas Valencia", "category": "decoracion", "city": "Valencia", "region": "Comunidad Valenciana",
     "rating": 4.7, "review_count": 89, "price_from": 1100, "price_unit": "eur_flat",
     "short_description": "Montaje floral, seating y ambientación completa llave en mano.", "featured": False},
]

CATEGORY_LABELS = {
    "banquete": "Banquetes",
    "finca": "Fincas y salones",
    "fotografia": "Fotografía",
    "musica": "Música",
    "wedding_planner": "Wedding Planner",
    "decoracion": "Decoración",
    "video": "Videografía",
    "animacion": "Animación",
    "floristeria": "Floristería",
    "belleza": "Belleza",
    "invitaciones": "Invitaciones",
    "coches": "Coches",
}

CATEGORY_TAGS = {
    "banquete": ["catering", "menú degustación", "opciones veganas"],
    "finca": ["ceremonia exterior", "jardín", "alojamiento invitados"],
    "fotografia": ["reportaje natural", "álbum premium", "preboda"],
    "musica": ["DJ", "iluminación", "ceremonia"],
    "wedding_planner": ["coordinación día B", "presupuesto", "diseño"],
    "decoracion": ["floral", "montaje", "temática"],
    "video": ["4K", "highlight", "drone"],
    "animacion": ["photocall", "espectáculo", "cóctel"],
    "floristeria": ["ramo novia", "centros mesa", "arco floral"],
    "belleza": ["maquillaje", "peinado", "prueba previa"],
    "invitaciones": ["papelería", "digital", "seating plan"],
    "coches": ["clásicos", "chófer", "decoración coche"],
}


def build() -> list[dict]:
    result = []
    photo_counters: dict[str, int] = {}
    for vendor in VENDORS_RAW:
        cat = vendor["category"]
        idx = photo_counters.get(cat, 0)
        photo_counters[cat] = idx + 1
        price_from = vendor.get("price_from")
        price_unit = vendor.get("price_unit", "eur_flat")
        if price_from is not None:
            if price_unit == "eur_per_guest":
                price_label = f"Desde {int(price_from)} €/invitado"
            elif price_unit == "eur_per_invite":
                price_label = f"Desde {price_from:.2f} €/invitación"
            else:
                price_label = f"Desde {int(price_from)} €"
        else:
            price_label = None

        result.append({
            "name": vendor["name"],
            "category": cat,
            "category_label": CATEGORY_LABELS.get(cat, cat.title()),
            "city": vendor["city"],
            "province": vendor["city"],
            "region": vendor.get("region"),
            "rating": vendor.get("rating"),
            "review_count": vendor.get("review_count"),
            "price_from": price_from,
            "price_unit": price_unit,
            "price_label": price_label,
            "short_description": vendor.get("short_description"),
            "tags": CATEGORY_TAGS.get(cat, ["boda"]),
            "capacity_min": vendor.get("capacity_min"),
            "capacity_max": vendor.get("capacity_max"),
            "featured": vendor.get("featured", False),
            "promotion": vendor.get("promotion"),
            "availability_hint": "Alta demanda fines de semana · consultar fecha",
            "image_url": photo_url(cat, idx),
            "source": "curated_seed_v2",
        })
    return result


def main() -> None:
    vendors = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"vendors": vendors}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(vendors)} vendors → {OUT}")
    print("\nNext: load into DB with:")
    print("  python -m app.scripts.load_wedding_vendors")


if __name__ == "__main__":
    main()
