from fastapi import FastAPI
from app.core.config import settings

app = FastAPI()


@app.get("/")
async def main():
    return {
        "message":200,
    }


@app.get("/info")
async def get_info():
    return {
        "DSN":settings.database_url
    }