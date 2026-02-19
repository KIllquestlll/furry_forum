# Connection main library
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete

# Import package
from app.models.post.categoryModel import CategoryModel
from app.schemas.post.categorySchema import CategoryScheme


async def createCategory(session:AsyncSession,
                         CategoryData:CategoryScheme) -> CategoryModel:
    
    query = select(CategoryModel).where(CategoryModel.title == CategoryData.title)
    result = await session.execute(query)
    existing_category = result.scalar_one_or_none()

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail="Категория с таким названием уже существует!"
        )


    new_category = CategoryModel(
        title=CategoryData.title,
    )
    session.add(new_category)

    try:
        await session.commit()
        await session.refresh(new_category)

        return new_category
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"{str(e)}"
        )
    
async def GettingAllCategory(session:AsyncSession) -> CategoryModel:

    query = select(CategoryModel).order_by(CategoryModel.id)
    result = await session.execute(query)

    category = result.scalars().all()

    return category


async def GettingByIdCategory(session:AsyncSession,
                              CategoryID:int) -> CategoryModel:

    query = select(CategoryModel).where(CategoryModel.id == CategoryID)
    result = await session.execute(query)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Роли с таким id не существует!"
        )
    return category



async def DeleteByIdCategory(session:AsyncSession,
                             CategoryID:int) -> dict:
    
    query = select(CategoryModel).where(CategoryModel.id == CategoryID)
    result = await session.execute(query)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Категории с таким названием нет!"
        )
    await session.delete(category)
    await session.commit()

    return {
        "status":"success",
        "message":f"{CategoryID} has been deleted"
    }

async def UpdateByIdCategory(session:AsyncSession,
                             CategoryData:CategoryScheme,
                             CategoryID:int):
    
    query = select(CategoryModel).where(CategoryModel.id == CategoryID)
    result = await session.execute(query)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Категории с таким id нет!"
        )
    
    update_data = CategoryData.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        setattr(category,key,value)

    try:
        await session.commit()
        await session.refresh(category)

        return category
    
    except Exception as e:
        await session.rollback()
        
        raise HTTPException(
            status_code=400,
            detail=f"Update failed {str(e)}"
        )