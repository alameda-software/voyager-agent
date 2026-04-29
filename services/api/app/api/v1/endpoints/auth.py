from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
async def login():
    # TODO: implement
    return {"message": "not implemented"}


@router.post("/register")
async def register():
    # TODO: implement
    return {"message": "not implemented"}
