# Connection main library
from pydantic import BaseModel,Field,EmailStr,model_validator,ConfigDict
from typing_extensions import Self

# Import package
from app.schemas.user.roleScheme import role


# Create User Scheme
class UserCreate(BaseModel):
    username:str
    password:str = Field(min_length=6)
    password_repeat:str = Field(min_length=6)
    email:EmailStr

    @model_validator(mode="after")
    def checker_password_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError("Doesn't match!")
        return self
    
    class Config:
        from_attributes = True


# Show users or user
class UserShow(BaseModel):
    username:str
    password:str
    email:EmailStr
    is_banned:bool
    role:role


# Lil users scheme
class UserRead(BaseModel):
    id: int
    username: str
    email: str
    role_title: str  
    is_banned: bool

    model_config = ConfigDict(from_attributes=True)

# Create users response
class UserCreateResponse(BaseModel):
    user:UserRead
    access_token:str
    token_type:str = "bearer"
