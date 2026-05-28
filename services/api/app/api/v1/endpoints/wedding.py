from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.domains.wedding.inventory import list_categories, search_vendors
from app.schemas.wedding import VendorCategoryRead, VendorSearchResponse

router = APIRouter()


@router.get("/categories", response_model=list[VendorCategoryRead])
async def get_wedding_categories(db: AsyncSession = Depends(get_db)):
    """Bodas.net-style vendor categories for the wedding MVP."""
    return await list_categories(db)


@router.get("/vendors", response_model=VendorSearchResponse)
async def search_wedding_vendors(
    category: Optional[str] = Query(None, description="Category id, e.g. finca, musica"),
    city: Optional[str] = Query(None, description="City name, e.g. Sevilla"),
    q: Optional[str] = Query(None, description="Free-text search"),
    limit: int = Query(12, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    results = await search_vendors(category=category, city=city, query=q, limit=limit, db=db)
    return VendorSearchResponse(
        total=len(results),
        category=category,
        city=city,
        query=q,
        results=results,
    )


@router.get("/vendors/stats")
async def wedding_vendor_stats(db: AsyncSession = Depends(get_db)):
    from app.domains.wedding.inventory import load_vendors
    vendors = await load_vendors(db)
    cities = sorted({v["city"] for v in vendors})
    categories = await list_categories(db)
    return {
        "vendor_count": len(vendors),
        "cities": cities,
        "categories": [c.id for c in categories],
        "source_note": (
            "MVP catalog inspired by bodas.net/proveedores. "
            "Live scraping is blocked (403); regenerate with scripts/generate_bodas_vendor_seed.py"
        ),
    }
