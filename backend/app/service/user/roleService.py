# Connection main library
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete

# Import package
from app.models.user.roleModel import RoleModel
from app.schemas.user.roleScheme import role


async def create_new_role(session:AsyncSession,roleData:role) -> RoleModel:

    query = select(RoleModel).where(RoleModel.title == roleData.title)
    result = await session.execute(query)
    existing_role = result.scalar_one_or_none()

    if existing_role:
        raise HTTPException(
            status_code=400,
            detail="Роль с таким названием уже существует"
        )

    # Create Model
    new_role = RoleModel(
        title=roleData.title
        )
    
    session.add(new_role)

    try:
        # Add 'n update
        await session.commit()
        await session.refresh(new_role)
        return new_role
    
    except Exception as e:
        await session.rollback()
        raise e
    
async def get_all_role(session:AsyncSession):
    # Query for showing all roles
    query = select(RoleModel).order_by(RoleModel.id)
    result = await session.execute(query)

    roles = result.scalars().all()

    return roles

async def get_by_id_role(session:AsyncSession,RoleID:int):
    query = select(RoleModel).where(RoleModel.id == RoleID)
    result = await session.execute(query)
    role_obj = result.scalar_one_or_none()

    if not role_obj:
        raise HTTPException(
            status_code=404,
            detail="Такого юзера не существует!"
        )

    return role_obj


async def delete_by_id(session:AsyncSession,roleID:int) -> dict[str,str]:

    query = select(RoleModel).where(RoleModel.id == roleID)
    result = await session.execute(query)
    role_obj = result.scalar_one_or_none()

    if not role_obj:
        raise HTTPException(
            status_code=404,
            detail=f"Din't found role"
        )
    
    await session.delete(role_obj)
    await session.commit()
    
    return {
        "status":"success",
        "message":f"Role:{roleID} has been deleted"
    }


async def update_by_id(session:AsyncSession,roleData:role,roleID:int) -> RoleModel:

    query = select(RoleModel).where(RoleModel.id == roleID)
    result = await session.execute(query)
    role_obj = result.scalar_one_or_none()

    if not role_obj:
        raise HTTPException(
            status_code=404,
            detail="Role not found"
        )
    
    # Convert data from dict,exclude that don't sent
    update_data = roleData.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        setattr(role_obj,key,value)

    try:
        await session.commit()
        await session.refresh(role_obj)

        return role_obj
    
    except Exception as e:
        await session.rollback()
        
        raise HTTPException(
            status_code=400,
            detail=f"Update failed:{str(e)}"
        )