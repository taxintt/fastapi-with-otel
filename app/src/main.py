from fastapi import FastAPI
from src.routers import hoge

app = FastAPI()
app.include_router(hoge.router)

