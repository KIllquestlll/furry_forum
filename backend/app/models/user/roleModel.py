# Connection main library
from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column

# Import base class
from app.db.database import Base


# Create model roles
class Role(Base):
    __tablename__ = "role"


    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(10),unique=True)
