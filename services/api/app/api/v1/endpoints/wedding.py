from typing import Optional

from fastapi import APIRouter, Query

from app.domains.wedding.inventory import list_categories, load_vendors, search_vendors
from app.schemas.wedding import VendorCategoryRead, VendorSearchResponse

router = APIRouter()


@router.get("/categories", response_model=list[VendorCategoryRead])
async def get_wedding_categories():
    """Bodas.net-style vendor categories for the wedding MVP."""
    return list_categories()


@router.get("/vendors", response_model=VendorSearchResponse)
async def search_wedding_vendors(
    category: Optional[str] = Query(None, description="Category id, e.g. finca, musica"),
    city: Optional[str] = Query(None, description="City name, e.g. Sevilla"),
    q: Optional[str] = Query(None, description="Free-text search"),
    limit: int = Query(12, ge=1, le=50),
):
    results = search_vendors(category=category, city=city, query=q, limit=limit)
    return VendorSearchResponse(
        total=len(results),
        category=category,
        city=city,
        query=q,
        results=results,
    )


@router.get("/vendors/stats")
async def wedding_vendor_stats():
    vendors = load_vendors()
    cities = sorted({vendor["city"] for vendor in vendors})
    categories = list_categories()
    return {
        "vendor_count": len(vendors),
        "cities": cities,
        "categories": categories,
        "source_note": (
            "MVP catalog inspired by bodas.net/proveedores. "
            "Live scraping is blocked (403); regenerate with scripts/generate_bodas_vendor_seed.py"
        ),
    }
