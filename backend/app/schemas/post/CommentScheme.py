from pydantic import BaseModel,ConfigDict
from typing import List,Optional

class CommentRead(BaseModel):
    id:int
    text:str
    author_id:int
    parent_id:Optional[int] = None
    replies:List["CommentRead"] = []

    model_config = ConfigDict(from_attributes=True)

class CommentCreate(BaseModel):
    text:str
    parent_id:Optional[int] = None

CommentRead.model_rebuild()