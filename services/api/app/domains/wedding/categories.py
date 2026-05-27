from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VendorCategory:
    id: str
    label: str
    description: str
    icon: str
    bodas_path: str


# Mirrors the public Bodas.net proveedores hub structure (category names & grouping).
WEDDING_VENDOR_CATEGORIES: tuple[VendorCategory, ...] = (
    VendorCategory(
        id="banquete",
        label="Banquetes",
        description="Catering y menús para tu banquete de boda.",
        icon="restaurant",
        bodas_path="/banquetes",
    ),
    VendorCategory(
        id="finca",
        label="Fincas y salones",
        description="Espacios para celebrar la ceremonia y el banquete.",
        icon="business",
        bodas_path="/fincas",
    ),
    VendorCategory(
        id="fotografia",
        label="Fotógrafos",
        description="Profesionales que inmortalizan vuestro gran día.",
        icon="camera",
        bodas_path="/fotografos",
    ),
    VendorCategory(
        id="video",
        label="Vídeo",
        description="Vídeos de boda, trailers y reportajes.",
        icon="videocam",
        bodas_path="/video",
    ),
    VendorCategory(
        id="musica",
        label="Música",
        description="DJs, bandas, coros y música en directo.",
        icon="musical-notes",
        bodas_path="/musica",
    ),
    VendorCategory(
        id="animacion",
        label="Animación",
        description="Entretenimiento y animación para invitados.",
        icon="sparkles",
        bodas_path="/animacion",
    ),
    VendorCategory(
        id="decoracion",
        label="Decoración",
        description="Ambientación floral y decoración de espacios.",
        icon="flower",
        bodas_path="/decoracion",
    ),
    VendorCategory(
        id="floristeria",
        label="Floristerías",
        description="Ramos, centros de mesa y decoración floral.",
        icon="rose",
        bodas_path="/floristerias",
    ),
    VendorCategory(
        id="wedding_planner",
        label="Wedding planners",
        description="Organización integral y coordinación del día B.",
        icon="calendar",
        bodas_path="/wedding-planners",
    ),
    VendorCategory(
        id="coches",
        label="Coches de boda",
        description="Transporte clásico y moderno para la pareja.",
        icon="car",
        bodas_path="/coches-de-boda",
    ),
    VendorCategory(
        id="belleza",
        label="Belleza novias",
        description="Peluquería, maquillaje y cuidado pre-boda.",
        icon="color-palette",
        bodas_path="/belleza-novias",
    ),
    VendorCategory(
        id="invitaciones",
        label="Invitaciones",
        description="Papelería, invitaciones digitales y seating.",
        icon="mail",
        bodas_path="/invitaciones",
    ),
)

CATEGORY_BY_ID = {item.id: item for item in WEDDING_VENDOR_CATEGORIES}

CATEGORY_ALIASES: dict[str, str] = {
    "banquetes": "banquete",
    "catering": "banquete",
    "menu": "banquete",
    "fincas": "finca",
    "salon": "finca",
    "salón": "finca",
    "venue": "finca",
    "lugar": "finca",
    "fotografo": "fotografia",
    "fotógrafo": "fotografia",
    "fotografos": "fotografia",
    "fotógrafos": "fotografia",
    "photo": "fotografia",
    "dj": "musica",
    "banda": "musica",
    "musica": "musica",
    "música": "musica",
    "animador": "animacion",
    "animación": "animacion",
    "decoracion": "decoracion",
    "decoración": "decoracion",
    "flores": "floristeria",
    "floristeria": "floristeria",
    "floristería": "floristeria",
    "planner": "wedding_planner",
    "organizador": "wedding_planner",
    "coche": "coches",
    "transporte": "coches",
    "maquillaje": "belleza",
    "peluqueria": "belleza",
    "peluquería": "belleza",
    "invitacion": "invitaciones",
    "invitación": "invitaciones",
    "video": "video",
    "vídeo": "video",
}
