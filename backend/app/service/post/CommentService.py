# Connection main library
from fastapi import HTTPException,UploadFile,Form,File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from sqlalchemy import select,delete,exists

# Connection other library


# Import package
from app.schemas.post.CommentScheme import CommentRead,CommentCreate
from app.models.post.postModel import PostModel
from app.models.post.CommentModel import CommentModel
from app.models.user.userModel import UserModel
from app.db.database import get_db

async def create_comment(session:AsyncSession,userID:UserModel,
                         commentData:CommentCreate,postID:int):
    
    post_check = await session.get(PostModel,postID)
    if not post_check:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    
    if commentData.parent_id == 0:
        commentData.parent_id = None

    if commentData.parent_id:
        parent_comment = await session.get(CommentModel,commentData.parent_id)

        if not parent_comment:
            raise HTTPException(
                status_code=404,
                detail="Parent comment is not found"
            )
        
        if parent_comment.post_id != postID:
            raise HTTPException(
                status_code=400,
                detail="НЕльзя отвечать на комментарии из других постов!"
            )
        

    new_comment = CommentModel(
        text=commentData.text,
        post_id=postID,
        author_id=userID.id,
        parent_id=commentData.parent_id,
    )

    session.add(new_comment)

    try:
        await session.commit()
        await session.refresh(new_comment)

        stmt = (
            select(CommentModel)
            .options(
                selectinload(CommentModel.author),
                selectinload(CommentModel.replies) 
            )
            .where(CommentModel.id == new_comment.id)
        )

        result = await session.execute(stmt)
        return result.scalar_one()
    
    except Exception as e:
        await session.rollback()
        print(f"DATABASE ERROR: {e}") 
        raise HTTPException(
            status_code=500,
            detail="Internal error"
        )
    

async def show_all_comment(session:AsyncSession):

    query = select(CommentModel)
    result = await session.execute(query)
    comments = result.scalars().all()

    if not comments:
        raise HTTPException(
            status_code=404,
            detail="Нет комментариев!"
        )
    
    return comments