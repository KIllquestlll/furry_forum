# Connetion main library
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,ForeignKey

# Import package
from app.db.database import Base


class PostMediaModel(Base):
    __tablename__ = "post_media"

    id:Mapped[int] = mapped_column(primary_key=True)

    file_path:Mapped[str] = mapped_column(String(500),nullable=False)
    file_type:Mapped[str] = mapped_column(String(20))

    post_id:Mapped[int] = mapped_column(ForeignKey("posts.id",ondelete="CASCADE"))
    post:Mapped["PostModel"] = relationship(back_populates="media")