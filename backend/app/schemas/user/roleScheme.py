# Connection main library
from pydantic import BaseModel,ConfigDict


# Create scheme role
class role(BaseModel):
    title: str = "guest"

    model_config = ConfigDict(from_attributes=True)

