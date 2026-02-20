# Connection main library
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,Depends,Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import joinedload
from jose import JWTError,jwt
from sqlalchemy import select,or_


# Import package
from app.schemas.user.userScheme import UserCreate
from app.models.user.userModel import UserModel
from app.core.security import get_password_hash,verify_password
from app.core.config import settings
from app.db.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

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

async def get_token(request:Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )
    return token


async def get_current_user(token:str = Depends(get_token),
                           session:AsyncSession = Depends(get_db),) -> UserModel:
    
    credentials_exception = HTTPException(
        status_code=401,
        detail="COuld not validate credential",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        user_id:str = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    query = select(UserModel).where(UserModel.id == int(user_id))
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user 
