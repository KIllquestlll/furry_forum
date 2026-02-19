# Connection main library
from pydantic import BaseModel,Field


class CategoryScheme(BaseModel):
    title: str = Field(min_length=2,max_length=20,description="Name category")
    