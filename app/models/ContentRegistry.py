from app.core.database import Base

from sqlalchemy.orm import Mapped, mapped_column

class ContentRegistry(Base):
    __tablename__: str = "content"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
