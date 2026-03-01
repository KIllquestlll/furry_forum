# Connection main library
from fastapi import HTTPException,UploadFile,Form,File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select,delete,exists,func

# Connection Other library
from aiofiles import open as aio_open 
import os
import uuid

# Import package
from app.schemas.post.postScheme import *
from app.models.post.postModel import PostModel
from app.models.user.userModel import UserModel
from app.models.post.LikeModel import LikeModel
from app.models.post.categoryModel import CategoryModel
from app.models.post.postMediaModel import PostMediaModel
from app.core.utils import generate_unique_slug



async def addLike(session:AsyncSession,postID:int,userID):
    query = select(LikeModel).where(
        LikeModel.post_id == postID,
        LikeModel.user_id == userID
    )

    result = await session.execute(query)
    like = result.scalar_one_or_none()

    if like:
        await session.delete(like)
        status = "removed"
        is_liked = False
    else:
        new_like = LikeModel(post_id=postID,user_id=userID)
        session.add(new_like)
        status = "add"
        is_liked = True
    await session.commit()

    сount_query = select(func.count()).select_from(LikeModel).where(LikeModel.post_id == postID)
    count_result = await session.execute(сount_query)
    total_likes = count_result.scalar()

    return{
        "status":status,
        "is_liked":is_liked,
        "total_likes":total_likes
    }