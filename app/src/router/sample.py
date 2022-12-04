import random
import time

from fastapi import APIRouter

sample_router = APIRouter()


@sample_router.get("/sample")
async def get_sample():
    time.sleep(2)
    return {"sample_id": random.randint(1, 10)}
