# Connetion main library
from sqlalchemy.orm import Mapped,mapped_column,relationship,column_property
from sqlalchemy import String,Text,ForeignKey,func,DateTime,select

# Connection other library
from typing import List,Optional
from datetime import datetime

# Import package
from app.db.database import Base


class PostModel(Base):
    __tablename__ = "posts"

    # Id fields
    id:Mapped[int] = mapped_column(primary_key=True)

    # String fields
    title:Mapped[str] = mapped_column(String(50),nullable=False)
    text:Mapped[str] = mapped_column(Text,nullable=False)
    slug:Mapped[str] = mapped_column(String(100),index=True,unique=True,nullable=False)

    # DateTime fields
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),index=True)

    # Many-to-many
    author_id:Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    author:Mapped["UserModel"] = relationship(back_populates="posts")

    # One-to-many
    media:Mapped[List["PostMediaModel"]] = relationship(
        back_populates="post",
        cascade="all,delete-orphan"
    )

    category:Mapped["CategoryModel"] = relationship(back_populates="post")
    category_id:Mapped[int] = mapped_column(ForeignKey("category.id",
                                            ondelete="SET NULL"),
                                            nullable=False)
    
    comments:Mapped[List["CommentModel"]] = relationship(
        back_populates="post",
        cascade="all,delete-orphan",
    )

    likes:Mapped[list["LikeModel"]] = relationship(back_populates="post",cascade="all,delete-orphan")