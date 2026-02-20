# Connection main library
from pydantic import BaseModel,ConfigDict

# Connetion other library
from typing import List,Optional
from datetime import datetime


class MediaRead(BaseModel):
    id:int
    file_path:str
    file_type:str

    model_config = ConfigDict(from_attributes=True)
    

class AuthorShorts(BaseModel):
    id:int
    username:str

    model_config = ConfigDict(from_attributes=True)


class PostBase(BaseModel):
    title:str
    text:str


class PostCreate(PostBase):
    pass


class PostRead(PostBase):
    id:int
    author:AuthorShorts
    created_at:datetime
    media:List[MediaRead] = []

    model_config = ConfigDict(from_attributes=True)