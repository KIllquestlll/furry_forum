# Connection main library
from fastapi import APIRouter,Depends,Response,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


# Connection other library
from typing import Annotated

# Import package
from app.schemas.user.userScheme import *
from app.service.user.authService import create_new_user,authenticate_user
from app.core.security import create_access_token
from app.db.database import get_db


# Router for connection
router = APIRouter(prefix="/api/auth",tags=["Auth"])

# Depends injection
AsyncDepends = Annotated[AsyncSession,Depends(get_db)]

# Registery route
@router.post("/register",response_model=UserCreateResponse)
async def register(userData:UserCreate,session:AsyncDepends,response:Response) -> dict:
    new_user = await create_new_user(session,userData)

    token_data = {"sub":str(new_user.id)}
    access_token = create_access_token(data=token_data)


    response.set_cookie(
        key="access_token", 
        value=access_token, # access_token or bearer
        httponly=True,      # Security of XXS
        max_age=3600 * 24,  # validity period
        samesite="lax",     # Base defance
        secure=False        # Turn on if HTTPS
    )


    return {
        "user":new_user,
        "access_token":access_token,
        "token_type":"bearer",
    }



# Login route
@router.post("/login",response_model=UserCreateResponse)
async def login(userData:UserCreate,session:AsyncDepends,response:Response):
    user = await authenticate_user(session,userData)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token_data = {"sub":str(user.id)}
    access_token = create_access_token(data=token_data)

    response.set_cookie(
        key="access_token", 
        value=access_token, # access_token or bearer
        httponly=True,      # Security of XXS
        max_age=3600 * 24,  # validity period
        samesite="lax",     # Base defance
        secure=False        # Turn on if HTTPS
    )

    return {
        "user":user,
        "access_token":access_token,
        "token_type":"bearer",
    }


@router.post("/logout")
async def logout(response:Response) -> dict[str,str]:
    response.delete_cookie("access_token")
    return {
        "message":"Logged out"
    }