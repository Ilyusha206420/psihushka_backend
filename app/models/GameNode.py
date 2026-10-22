from sqlalchemy import ForeignKey, Integer

from app.core.database import Base
from app.core.constants import Methods

from sqlalchemy.orm import Mapped, mapped_column

class GameNode(Base):
    __tablename__:str = "game_nodes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    method_id: Mapped[Methods] = mapped_column(
        Integer,
        ForeignKey("event_method_dict.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    data_id: Mapped[int | None] = mapped_column(ForeignKey("content.id", ondelete="CASCADE", onupdate="CASCADE"))
