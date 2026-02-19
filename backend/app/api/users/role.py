# Connection main library
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List,Optional,Annotated

# Import package
from app.schemas.user.roleScheme import role
from app.db.database import get_db
from app.models.user.roleModel import RoleModel
from app.service.user.roleService import *


# Router for role handlers
router = APIRouter(prefix="/api/role",
                 tags=["RolePanel"])

AsyncDepends = Annotated[AsyncSession,Depends(get_db)]

# POST query
@router.post("/create")
async def createRole(roleData:role,session:AsyncDepends):
    try:
        result = await create_new_role(session,roleData)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )
        
    


# GET query
@router.get("/show")
async def get_all_roles(session:AsyncDepends):
    try:
        result = await get_all_role(session)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"{str(e)}"
        )


@router.get("/show/{id}")
async def get_id_role(session:AsyncDepends,RoleID:int):
    return await get_by_id_role(session,RoleID)
    


# DELETE query
@router.delete("/delete/{id}")
async def delete_by_roles(session:AsyncDepends,roleID:int):
    return await delete_by_id(session,roleID)




# PATCH query
@router.patch("/update/{id}",response_model=role)
async def update_by_roles(session:AsyncDepends,roleData:role,roleID:int):
    return await update_by_id(session,roleData,roleID)




        

          
       

        

