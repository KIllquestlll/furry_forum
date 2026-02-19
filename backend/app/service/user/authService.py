# Connection main library
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy import select,or_


# Import package
from app.schemas.user.userScheme import UserCreate
from app.models.user.userModel import UserModel
from app.core.security import get_password_hash,verify_password

# Registery func
async def create_new_user(session: AsyncSession, userData: UserCreate) -> UserModel:
    # Checked username 'n email
    query = select(UserModel).where(
        or_(
            UserModel.username == userData.username,
            UserModel.email == userData.email,
        )
    )
    result = await session.execute(query)
    existing_user = result.scalars().first()

    # If username already exist we get errors
    if existing_user:
        detail = "Username already exists" if existing_user.username == userData.username else "Email already exists"
        raise HTTPException(status_code=400, detail=detail)
    
    # Change password of hashed_password
    hashed_password = get_password_hash(userData.password)
    user_data_dict = userData.model_dump(exclude={"password_repeat", "password"})
    
    # Creating new users
    new_user = UserModel(
        **user_data_dict,
        password=hashed_password,
        is_banned=False,
        role_id=4  
    )

    session.add(new_user)

    try:
        await session.commit()
        # Join
        query_refresh = select(UserModel).options(joinedload(UserModel.role)).where(UserModel.id == new_user.id)
        await session.refresh(new_user, ["role"]) 
        
        return new_user
    
    except Exception as e:
        await session.rollback()

        raise HTTPException(
            status_code=500,
            detail="Internal server error during user creation"
        )
    

# Login users func 
async def authenticate_user(session:AsyncSession,userData:UserCreate):
    query = (
        select(UserModel)
        .options(joinedload(UserModel.role)) 
        .where(UserModel.username == userData.username)
    )
    result = await session.execute(query)

    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
        return False
    if not verify_password(userData.password,user.password):
        return False
    
    return user
