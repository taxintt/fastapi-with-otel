from fastapi import FastAPI
from routers import hoge

app = FastAPI()
app.include_router(hoge.router)

