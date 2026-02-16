# Connection main library
from fastapi import APIRouter

# Router for Category handlers
router = APIRouter(prefix="/category",
                     tags=["CategoryPanel"])