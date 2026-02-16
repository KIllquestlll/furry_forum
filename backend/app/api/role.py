# Connection main library
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List,Optional,Annotated

# Import package
from app.schemas.user.roleScheme import role
from app.db.database import get_db
from app.models.user.roleModel import Role


# Router for role handlers
router = APIRouter(prefix="/role",
                 tags=["RolePanel"])

AsyncDepends = Annotated[AsyncSession,Depends(get_db)]

class RoleHandler:

    def __init__(self,session:AsyncSession):
        self.session =  session

    @router.post("/create")
    async def createRole(self,roleData:role,session:AsyncDepends) -> role:
        
       new_Role = Role(
           title=roleData.title,
       )

       session.add(new_Role)

       try:
           await session.commit()
           await session.refresh(new_Role)

           return role
       
       except Exception as e:
          
          await session.rollback(new_Role)

          raise HTTPException(
              status_code=400,
              detail=f"Ops,did't created role:{str(e)}"
          )
       return role

    @router.get("/role/show")
    async def get_all_roles(self,session:AsyncDepends):

        query = select(Role).order_by(Role.id)
        result = await session.execute(query)

        roles = result.scalars().all()

        return roles

        

          
       

        

