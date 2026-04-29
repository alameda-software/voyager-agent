from fastapi import APIRouter

router = APIRouter()


@router.post("/flights")
async def search_flights():
    # TODO: implement via Amadeus
    return {"message": "not implemented"}


@router.post("/hotels")
async def search_hotels():
    # TODO: implement via Amadeus
    return {"message": "not implemented"}
