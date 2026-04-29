from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

from app.services.letsfg import LetsFGService
from app.services.swoop import SwoopService

router = APIRouter()


class FlightSearchParams(BaseModel):
    origin: str  # IATA code
    destination: str  # IATA code
    date: str  # YYYY-MM-DD
    return_date: Optional[str] = None
    adults: int = 1
    cabin: str = "economy"
    max_stops: Optional[int] = None


class HotelSearchParams(BaseModel):
    city: str
    check_in: str  # YYYY-MM-DD
    check_out: str  # YYYY-MM-DD
    adults: int = 1


@router.post("/flights")
async def search_flights(params: FlightSearchParams):
    """Search flights via LetsFG."""
    service = LetsFGService()
    result = await service.search(
        origin=params.origin,
        destination=params.destination,
        date=params.date,
        return_date=params.return_date,
        adults=params.adults,
        cabin=params.cabin,
        max_stops=params.max_stops,
    )
    return result


@router.post("/hotels")
async def search_hotels(params: HotelSearchParams):
    """Search hotels (stub — swoop integration coming)."""
    return {
        "error": "Hotel search not yet implemented",
        "results": [],
    }


@router.get("/locations")
async def resolve_location(query: str):
    """Resolve a city name to IATA codes."""
    service = LetsFGService()
    results = await service.locations(query)
    return results
