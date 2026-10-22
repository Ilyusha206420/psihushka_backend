from app.core.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
 
class TextContent(Base):
    __tablename__: str = "texts"

    id: Mapped[int] = mapped_column(
        ForeignKey("content_registry", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True
    )
    text: Mapped[str] = mapped_column(unique=True)
