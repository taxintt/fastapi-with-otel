from fastapi import APIRouter

router = APIRouter()


@router.get("/hoge")
async def hoge():
    return {"message": "return hoge"}
