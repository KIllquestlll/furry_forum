# Connection main library
from fastapi import APIRouter,Depends

# Connection other library
from typing import Annotated

# Import package
from app.schemas.post.CommentScheme import CommentRead,CommentCreate
from app.service.user.authService import get_current_user
from app.models.user.userModel import UserModel
from app.service.post.CommentService import *
from app.db.database import AsyncSession,get_db

router = APIRouter(prefix="/api/comment",tags=["comment"])
AsyncDepends = Annotated[AsyncSession,Depends(get_db)]



# POST-query
@router.post("/{post_id}/",response_model=CommentRead)
async def CreateComment(post_id:int,commentData:CommentCreate,
                        session:AsyncDepends,
                        current_user:UserModel = Depends(get_current_user)):
    
    return await create_comment(session,current_user,commentData,post_id)


# GET-query
@router.get("/show")
async def ShowAllComment(session:AsyncDepends):
    return await show_all_comment(session)