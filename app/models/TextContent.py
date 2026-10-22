from app.core.database import Base

from sqlalchemy.orm import Mapped, mapped_column

 
class TextContent(Base):
    __table_name__: str = "texts"

    id: Mapped[int] = mapped_column(
        ForeignKey("content_registry", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True
    )
    text: Mapped[str] = mapped_column(unique=true)

        def __init__(text: str):
            new_reg = ContentRegistry()
            self.id = new_reg.id
            self.text = text
