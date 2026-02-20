# Connection main library
from fastapi import APIRouter,Depends,Response,HTTPException,UploadFile,Form,File
from sqlalchemy.ext.asyncio import AsyncSession


# Connection other library
from typing import Annotated

# Import package
from app.schemas.post.postScheme import PostRead
from app.models.user.userModel import UserModel
from app.service.post.postService import *
from app.service.user.authService import get_current_user
from app.db.database import get_db

# Router for connection
router = APIRouter(prefix="/api/post",tags=["Post"])

# Depends injection
AsyncDepends = Annotated[AsyncSession,Depends(get_db)]


# POST-query
@router.post("/create", response_model=PostRead)
async def CreatePost(
    title: str = Form(...),
    text: str = Form(...),
    files: List[UploadFile] = File(None), 
    session: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    post_data = PostCreate(title=title, text=text)
    
    return await create_new_post(session, post_data, current_user.id, files)

# GET-query
@router.get("/show")
async def ShowAllPosts(session:AsyncDepends):
    return await show_all_post(session)



# DELETE-query
@router.delete("/delete/all")
async def DeleteAllPost(session:AsyncDepends):
    return await delete_all_posts(session)