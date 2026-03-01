from fastapi import Depends,HTTPException

# Import other library
from slugify import slugify
import uuid

# Import package
from app.schemas.user.userScheme import UserRead
from app.service.user.authService import get_current_user

# Generate slug
def generate_unique_slug(text:str) -> str:
    base_slug = slugify(text)

    unique_id = uuid.uuid4().hex[:6]
    return f"{base_slug}-{unique_id}"



# CheckRole
class RoleChecker:
    def __init__(self,allowed_roles:list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(self, user:UserRead = Depends(get_current_user)):
        if user.role_title not in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="У вас недостаточно прав!"
            )
        return user
    
allow_admin = RoleChecker(["admin"])