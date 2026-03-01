# Connection main library
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,Text,ForeignKey,func,DateTime

from typing import List,Optional

# Import package
from app.db.database import Base


class CommentModel(Base):
    __tablename__ = "comments"
    
    # Integer fields
    id:Mapped[int] = mapped_column(primary_key=True)

    # String fields
    text:Mapped[str] = mapped_column(Text,nullable=False)

    # RelationShip
    post_id:Mapped[int] = mapped_column(ForeignKey("posts.id",ondelete="CASCADE"))
    author_id:Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    author: Mapped["UserModel"] = relationship(back_populates="comments")
    post: Mapped["PostModel"] = relationship(back_populates="comments")

    parent_id:Mapped[Optional[int]] = mapped_column(
        ForeignKey("comments.id",ondelete="CASCADE"),nullable=True
    )


    replies:Mapped[List["CommentModel"]] = relationship(
        back_populates="parent",
        cascade="all,delete-orphan",
        single_parent=True,
        remote_side=[parent_id]
    )

    parent:Mapped[Optional["CommentModel"]] = relationship(
        back_populates="replies",
        remote_side=[id]
    )