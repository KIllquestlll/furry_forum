# Connection main library
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String
# Import package
from app.db.database import Base


class CategoryModel(Base):
    # Named table
    __tablename__ = "category"

    # Integer fields
    id: Mapped[int] = mapped_column(primary_key=True)

    # String fields
    title:Mapped[str] = mapped_column(String(20),nullable=False,unique=True)
    