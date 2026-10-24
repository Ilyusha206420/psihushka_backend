from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core import Base
from app.models.Node import Node

class Edge(Base):
    __tablename__:str = "edges"

    src_id: Mapped[int] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    tgt_id: Mapped[int] = mapped_column(
        ForeignKey("nodes.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )

    tgts: Mapped[Node] = relationship(foreign_keys=[tgt_id])
