# Connection main library
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
# Connection other library
from typing import Annotated


# Import package
from app.service.user.userService import get_all_users,get_by_id_user
from app.db.database import get_db


# Router for connection
router = APIRouter(prefix="/api/user",tags=["User"])

# Depends injection
AsyncDepends = Annotated[AsyncSession,Depends(get_db)]


# Show all users route
@router.get("/user")
async def showUsers(session:AsyncDepends):
    return await get_all_users(session)


@router.get("/user/{id}")
async def ShowUserById(session:AsyncDepends,userID:int):
    return await get_by_id_user(session,userID)