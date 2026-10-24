from sqlalchemy.orm import Mapped, mapped_column
from app.core import Base

class Content(Base):
    __tablename__: str = "content"
    id: Mapped[int] = mapped_column(primary_key=True)
    data: Mapped[str] = mapped_column(unique=True)
