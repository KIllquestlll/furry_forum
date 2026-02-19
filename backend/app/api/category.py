# Connection main library
from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Import  other library
from typing import Annotated

# Import package
from app.db.database import get_db
from app.service.post.categoryService import *
from app.schemas.post.categorySchema import CategoryScheme

# Router for Category handlers
router = APIRouter(prefix="/api/category",
                     tags=["CategoryPanel"])


AsyncDepends = Annotated[AsyncSession,Depends(get_db)]

# POST query
@router.post("/create")
async def create_category(session:AsyncDepends,CategoryData:CategoryScheme):
    try:
        result = await createCategory(session,CategoryData)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )



# GET query
@router.get("/show")
async def get_all_category(session:AsyncDepends):
    return await GettingAllCategory(session)


@router.get("/show/{id}")
async def get_category_by_id(session:AsyncDepends,CategoryID:int):
    return await GettingByIdCategory(session,CategoryID)



# DELETE query
@router.delete("/delete/{id}")
async def delete_category_by_id(session:AsyncDepends,CategoryID:int):
    return await DeleteByIdCategory(session,CategoryID)



# PATCH query
@router.patch("/update/{id}")
async def update_category_by_id(session:AsyncDepends,CategoryData:CategoryScheme,CategoryID:int):
    return await UpdateByIdCategory(session,CategoryData,CategoryID)