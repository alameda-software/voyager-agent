# Wedding vendor catalog (MVP)

Bodas.net-style proveedores directory for local development.

## Data source

- **Live scrape**: `bodas.net` returns HTTP 403 to automated requests (httpx + Playwright).
- **MVP catalog**: `data/vendors.json` — synthetic listings with realistic fields (rating, reviews, price band, city, promotions).
- **Regenerate**: `python scripts/generate_bodas_vendor_seed.py`

## API

- `GET /api/v1/wedding/categories`
- `GET /api/v1/wedding/vendors?category=finca&city=Sevilla&q=...`
- `GET /api/v1/wedding/vendors/stats`

## Chat

Wedding domain pack returns `vendor_cards` in message payload when the user provides city + category or asks to search.

Example: *"Buscar fincas en Sevilla para 120 invitados"*
