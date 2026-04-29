from fastapi import APIRouter

router = APIRouter()


@router.post("/send")
async def send_message():
    # TODO: implement
    return {"message": "not implemented"}


@router.get("/history")
async def get_history():
    # TODO: implement
    return {"messages": []}
