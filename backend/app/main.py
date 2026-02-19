# Import main library
from fastapi import FastAPI,status
from fastapi.middleware.cors import CORSMiddleware

# Import Config 'n other
from app.core.config import settings

# Import router
from app.api.category import router as category
from app.api.users.auth import router as auth
from app.api.users.role import router as role
from app.api.users.users import router as user


origins = [
    "http://localhost:3000",     
]


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
    _app.include_router(auth)
    _app.include_router(user)

    return _app

app = get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Разрешить запросы с этих адресов
    allow_credentials=True,           # ОБЯЗАТЕЛЬНО для работы с куками!
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PUT"], # Разрешенные методы
    allow_headers=["Content-Type", "Set-Cookie", "Authorization"], # Разрешенные заголовки
)

@app.get("/ping")
async def ping() -> dict[str,str | list]:
    return {
        "status":"200",
        "DNS":settings.database_url,
        "DATA":[settings.ALGORITHM,
               settings.ACCESS_TOKEN_EXPIRE_MINUTES,
               settings.SECRET_KEY]
    }


