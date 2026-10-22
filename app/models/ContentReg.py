from app.core.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship

class ContentRegistry(Base):
    __tablename__: str = "content"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    text = relationship()
