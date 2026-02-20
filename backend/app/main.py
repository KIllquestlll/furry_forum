# Import main library
from fastapi import FastAPI,status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import Config 'n other
from app.core.config import settings

# Import router
from app.api.category import router as category
from app.api.users.auth import router as auth
from app.api.users.role import router as role
from app.api.users.users import router as user
from app.api.post.postAPI import router as post


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
    _app.include_router(post)

    return _app

app = get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,           
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PUT"], 
    allow_headers=["Content-Type", "Set-Cookie", "Authorization"], 
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/ping")
async def ping() -> dict[str,str | list]:
    return {
        "status":"200",
        "DNS":settings.database_url,
        "DATA":[settings.ALGORITHM,
               settings.ACCESS_TOKEN_EXPIRE_MINUTES,
               settings.SECRET_KEY]
    }


