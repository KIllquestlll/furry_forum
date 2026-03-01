# Connetion main library
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Text,ForeignKey,func,DateTime

# Connection other library
from typing import List,Optional
from datetime import datetime


# Import package
from app.db.database import Base

class LikeModel(Base):
    __tablename__ =  "likes"

    # Integer fields
    user_id:Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"),
                                        primary_key=True)
    post_id:Mapped[int] = mapped_column(ForeignKey("posts.id",ondelete="CASCADE"),
                                        primary_key=True)

    user: Mapped["UserModel"] = relationship(back_populates="liked_post")
    post: Mapped["PostModel"] = relationship(back_populates="likes")