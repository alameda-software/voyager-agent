#!/usr/bin/env python3
"""Generate MVP wedding vendor JSON inspired by bodas.net proveedores structure.

Live scraping from bodas.net is blocked (HTTP 403). Run this script to refresh
the local catalog used by the wedding domain. Names and copy are synthetic;
field shapes mirror typical Bodas.net listing cards.
"""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "app" / "domains" / "wedding" / "data" / "vendors.json"

CITIES = [
    ("Sevilla", "Andalucía"),
    ("Madrid", "Comunidad de Madrid"),
    ("Barcelona", "Cataluña"),
    ("Málaga", "Andalucía"),
    ("Valencia", "Comunidad Valenciana"),
]

TEMPLATES: dict[str, list[dict]] = {
    "banquete": [
        ("Catering {city} Deluxe", "Menús de autor con maridaje y servicio de sala incluido.", 72, 180),
        ("Banquetes La {city}", "Cocina mediterránea, opciones veganas y menú infantil.", 58, 220),
    ],
    "finca": [
        ("Finca Los Olivos · {city}", "Ceremonia al aire libre y salón con vistas al campo.", 85, 280),
        ("Hacienda {city} Events", "Capilla privada, jardín y suite nupcial para la pareja.", 110, 320),
    ],
    "fotografia": [
        ("Estudio {city} Weddings", "Reportaje natural, álbum premium y sesión preboda.", 1200, 45),
        ("FotoBoda {city}", "Cobertura completa con segundo fotógrafo y entrega en 30 días.", 890, 98),
    ],
    "musica": [
        ("DJ Bodas {city}", "Pack ceremonia + cóctel + fiesta con iluminación incluida.", 750, 156),
        ("Orquesta Noches de {city}", "Repertorio internacional y coordinación con maestro de ceremonias.", 1400, 62),
    ],
    "wedding_planner": [
        ("Wedding Studio {city}", "Coordinación integral, timeline y gestión de proveedores.", 1800, 74),
        ("Tu Boda en {city}", "Diseño conceptual, presupuesto y acompañamiento el día B.", 2200, 41),
    ],
    "decoracion": [
        ("Decor Events {city}", "Montaje floral, seating y ambientación de ceremonia.", 950, 53),
        ("Espacios {city} Design", "Decoración boho, clásica o mediterránea llave en mano.", 1200, 29),
    ],
    "animacion": [
        ("Showtime {city}", "Animación, photocall y espectáculo para cóctel y banquete.", 480, 88),
    ],
    "coches": [
        ("Clásicos {city}", "Rolls, Mercedes vintage y chófer con decoración floral.", 420, 112),
    ],
    "floristeria": [
        ("Flores de {city}", "Ramo de novia, botonier y centros de mesa personalizados.", 380, 67),
    ],
    "belleza": [
        ("Beauty {city} Brides", "Prueba de maquillaje y peinado con equipo a domicilio.", 220, 143),
    ],
    "invitaciones": [
        ("Papel & Detalle {city}", "Invitaciones impresas, seating plan y papelería coordinada.", 3.5, 34),
    ],
    "video": [
        ("CineBoda {city}", "Vídeo cinematográfico, highlight y entrega digital 4K.", 1350, 51),
    ],
}


def build_vendors() -> list[dict]:
    vendors: list[dict] = []
    idx = 0
    for city, region in CITIES:
        for category, items in TEMPLATES.items():
            for name_tpl, desc_tpl, price_from, reviews in items:
                idx += 1
                name = name_tpl.format(city=city)
                slug = f"{category}-{city.lower().replace('á', 'a')}-{idx}"
                unit = "eur_per_guest" if category in {"banquete", "finca"} else "eur_flat"
                if category == "invitaciones":
                    unit = "eur_per_invite"
                    price_label = f"Desde {price_from:.2f} €/invitación"
                elif unit == "eur_per_guest":
                    price_label = f"Desde {int(price_from)} €/invitado"
                else:
                    price_label = f"Desde {int(price_from)} €"

                rating = round(4.3 + (idx % 7) * 0.1, 1)
                vendors.append(
                    {
                        "id": slug,
                        "name": name,
                        "category": category,
                        "city": city,
                        "province": city,
                        "region": region,
                        "rating": min(rating, 5.0),
                        "review_count": reviews + (idx % 20),
                        "price_from": price_from,
                        "price_unit": unit,
                        "price_label": price_label,
                        "short_description": desc_tpl.format(city=city),
                        "tags": _tags(category),
                        "capacity_min": 50 if category == "finca" else None,
                        "capacity_max": 250 if category == "finca" else None,
                        "featured": idx % 5 == 0,
                        "promotion": "Promoción MVP: consulta disponibilidad sin compromiso" if idx % 4 == 0 else None,
                        "availability_hint": "Alta demanda fines de semana · consultar fecha",
                        "image_url": f"https://images.unsplash.com/photo-1519741497674-611481863552?w=800&q=80&sig={idx}",
                        "source": "mvp_seed",
                        "source_inspiration": "bodas.net/proveedores",
                    }
                )
    return vendors


def _tags(category: str) -> list[str]:
    mapping = {
        "banquete": ["catering", "menú degustación", "opciones veganas"],
        "finca": ["ceremonia exterior", "alojamiento invitados", "jardín"],
        "fotografia": ["reportaje natural", "álbum premium", "preboda"],
        "musica": ["DJ", "iluminación", "ceremonia"],
        "wedding_planner": ["coordinación día B", "presupuesto", "diseño"],
        "decoracion": ["floral", "montaje", "temática"],
        "animacion": ["photocall", "espectáculo", "cóctel"],
        "coches": ["clásicos", "chófer", "decoración coche"],
        "floristeria": ["ramo novia", "centros mesa", "arco floral"],
        "belleza": ["maquillaje", "peinado", "prueba previa"],
        "invitaciones": ["papelería", "digital", "seating plan"],
        "video": ["4K", "highlight", "drone opcional"],
    }
    return mapping.get(category, ["boda"])


def main() -> None:
    vendors = build_vendors()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"vendors": vendors}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(vendors)} vendors to {OUT}")


if __name__ == "__main__":
    main()
