# Connection main library
from fastapi import Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

# Import package
from app.models.user.userModel import UserModel


# This's package needed for func for CRUD on users
# authService must be logic for authentication


# Show all users func
async def get_all_users(session:AsyncSession) -> UserModel:
    query = (
        select(UserModel)
        .options(joinedload(UserModel.role))
        .order_by(UserModel.id)
    )
    result = await session.execute(query)

    users = result.scalars().all()

    if not users:
        raise HTTPException(
            status_code=404,
            detail="No users found"
        )

    return users

# Func for find user by id
async def get_by_id_user(session:AsyncSession,userID:int) -> UserModel:
    query = (
        select(UserModel)
        .options(joinedload(UserModel.role))
        .where(UserModel.id == userID)
    )
    result = await session.execute(query)

    user = result.scalar_one_or_none()

    return user


# Func for updating role user by id
async def update_role_by_id(session:AsyncSession,userID:int):
    pass