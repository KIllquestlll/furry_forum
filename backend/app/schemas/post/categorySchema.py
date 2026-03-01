# Connection main library
from pydantic import BaseModel,Field,ConfigDict


class CategoryScheme(BaseModel):
    title: str = Field(min_length=2,max_length=20,description="Name category")
    
class CategoryRead(BaseModel):
    title:str

    model_config = ConfigDict(from_attributes=True)