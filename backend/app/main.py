# Import main library
from fastapi import FastAPI

# Import Config 'n other
from app.core.config import settings

# Import router
from app.api.category import category
from app.api.role import role


# Create copy app
def get_app() -> FastAPI:

    _app = FastAPI(
        title="FurryForum",
        version="1.0.0",
        debug=settings.DEBUG,
    )

    # Connection other router
    _app.include_router(category)
    _app.include_router(role)

    return _app

app = get_app()

@app.get("/ping")
async def ping() -> dict[str,str | int]:
    return {
        "status":200,
        "DNS":settings.database_url,
    }


