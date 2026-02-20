# Connection main library
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# Connection other library
from typing import Annotated

# Import package
from app.schemas.user.userScheme import *
from app.service.user.userService import *
from app.db.database import get_db


# Router for connection
router = APIRouter(prefix="/api/user",tags=["User"])

# Depends injection
AsyncDepends = Annotated[AsyncSession,Depends(get_db)]


# GET-query
@router.get("/user")
async def showUsers(session:AsyncDepends):
    return await get_all_users(session)


@router.get("/user/{id}")
async def ShowUserById(session:AsyncDepends,userID:int):
    return await get_by_id_user(session,userID)


# DELETE-query
@router.delete("/delete/all")
async def DeleteAllUsers(session:AsyncDepends):
    return await delete_all_users(session)


# UPDATE-query
@router.patch("/update/role/{id}")
async def UpdateRoleByUserID(id:int,userData:UpdateRoleScheme,session:AsyncDepends):
    return await update_role_user_by_id(session,id,userData.new_role_id)
