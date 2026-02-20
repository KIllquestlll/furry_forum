# Connection main library
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import String,ForeignKey

# Connection other library
from typing import List,Optional

# Import package
from app.db.database import Base

class UserModel(Base):
    # Named table
    __tablename__ = "users"

    # Integer fields
    id:Mapped[int] = mapped_column(primary_key=True,)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), default=1)

    # String fields
    username:Mapped[str] = mapped_column(nullable=False)
    email:Mapped[str] = mapped_column(unique=True,nullable=False)
    password:Mapped[str] = mapped_column(nullable=False,)
    role_title: Mapped[str] = association_proxy("role", "title")

    # Bool fields
    is_banned:Mapped[bool] = mapped_column(default=False)

    # RelationShip fields
    role:Mapped["RoleModel"] = relationship(back_populates="users")
    posts:Mapped[List["PostModel"]] = relationship(back_populates="author")