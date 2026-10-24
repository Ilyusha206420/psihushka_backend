from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Base, Methods
from app.models.Content import Content

class Node(Base):
    __tablename__:str = "nodes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    method: Mapped[Methods] = mapped_column(Integer)
    cont_id: Mapped[int] = mapped_column(ForeignKey("content.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)

    data: Mapped[Content] = relationship()
    next_nodes: Mapped[list[Node]] = relationship(
        secondary="edges",
        primaryjoin="nodes.id == edges.src_id",
        secondaryjoin="nodes.id == edges.tgt_id",
        viewonly=True
    )

