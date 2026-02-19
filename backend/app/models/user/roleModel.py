# Connection main library
from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship

# Import package
from app.db.database import Base


# Create model roles
class RoleModel(Base):
    # Named table
    __tablename__ = "role"

    # Integer fields
    id: Mapped[int] = mapped_column(primary_key=True)

    # String fields
    title: Mapped[str] = mapped_column(String(10),unique=True)

    # RelationShip fields
    users:Mapped[list["UserModel"]] = relationship(back_populates="role")