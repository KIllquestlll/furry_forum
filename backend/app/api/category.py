# Connection main library
from fastapi import APIRouter

# Router for Category handlers
category = APIRouter(prefix="/category",
                     tags=["CategoryPanel"])