# Connection main library
from fastapi import APIRouter


# Router for role handlers
role = APIRouter(prefix="/role",
                 tags=["RolePanel"])