# Connection main library
from pydantic import BaseModel,ConfigDict

# Connetion other library
from typing import List,Optional
from datetime import datetime

# Import package
from app.schemas.post.categorySchema import CategoryRead
from app.schemas.post.CommentScheme import CommentRead


class MediaRead(BaseModel):
    file_path:str
    file_type:str

    model_config = ConfigDict(from_attributes=True)
    

class AuthorShorts(BaseModel):
    username:str

    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    title:str
    text:str


class PostCreate(PostBase):
    category_name:str


class PostRead(PostBase):
    id:int
    author:AuthorShorts
    created_at:datetime
    category:Optional[CategoryRead] = None
    comments:List[CommentRead]
    media:List[MediaRead] = []

    likes_count:int
    is_liked:bool = False

    model_config = ConfigDict(from_attributes=True)