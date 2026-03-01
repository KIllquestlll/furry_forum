# Connection main library
from fastapi import APIRouter,Depends,Response,HTTPException,UploadFile,Form,File
from sqlalchemy.ext.asyncio import AsyncSession


# Connection other library
from typing import Annotated

# Import package
from app.schemas.post.postScheme import PostRead
from app.models.user.userModel import UserModel
from app.schemas.user.userScheme import UserRead
from app.service.post.postService import *
from app.core.utils import RoleChecker,allow_admin
from app.service.user.authService import get_current_user
from app.service.post.LikeService import *
from app.db.database import get_db

router = APIRouter(prefix="/api/like")
AsyncDepends = Annotated[AsyncSession,Depends(get_db)]

@router.post("/add/{postID}")
async def add_like_post(session:AsyncDepends,postID:int,
                        current_user:UserRead = Depends(get_current_user)):
    return await addLike(session,postID,current_user.id)
