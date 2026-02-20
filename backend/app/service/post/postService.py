# Connection main library
from fastapi import HTTPException,UploadFile,Form,File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select,delete,exists

# Connection Other library
from aiofiles import open as aio_open 
import os
import uuid

# Import package
from app.schemas.post.postScheme import *
from app.models.post.postModel import PostModel
from app.models.post.postMediaModel import PostMediaModel
from app.core.utils import generate_unique_slug


# POST query
async def create_new_post(session:AsyncSession,
                          postData:PostCreate,
                          userId:int,
                          files:List[UploadFile] = None):
    
    slug = generate_unique_slug(postData.title)

    query = select(exists().where(PostModel.slug == slug))
    result = await session.execute(query)

    if result.scalar():
        raise HTTPException(
            status_code=400,detail="Slug already exists"
        )
    
    new_post = PostModel(
        title=postData.title,
        text=postData.text,
        slug=slug,
        author_id=userId,
    )

    try:
        session.add(new_post)
        await session.flush()

        if files:
            upload_dir = "static/uploads"
        os.makedirs(upload_dir, exist_ok=True)

        for file in files:
            
            file_ext = os.path.splitext(file.filename)[1]
            unique_name = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(upload_dir, unique_name)

            
            async with aio_open(file_path, mode='wb') as f:
                content = await file.read()
                await f.write(content)

            
            new_media = PostMediaModel(
                file_path=f"/{file_path}", 
                file_type=file.content_type,
                post_id=new_post.id
            )

            session.add(new_media)

        await session.commit()
        await session.refresh(new_post)

        stmt = (
            select(PostModel)
            .options(
                selectinload(PostModel.author),
                selectinload(PostModel.media)
            )
            .where(PostModel.id == new_post.id)
        )

        final_result = await session.execute(stmt)
        return final_result.scalar_one_or_none()
    
    except Exception as e:
        await session.rollback()
        print(f"Error {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
    
# GET-query
async def show_all_post(session:AsyncSession):
    query = select(PostModel)
    result = await session.execute(query)

    posts = result.scalars().all()

    return posts


# DELETE-query
async def delete_all_posts(session:AsyncSession):
    try:
        query = delete(PostModel)
        await session.execute(query)
        await session.commit()
        
        return {
            "Detail":"All posts have been deleted"
        }
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not deleted posts"
        )