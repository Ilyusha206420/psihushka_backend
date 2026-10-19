import zlib
from enum import Enum, auto
from typing import override

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.schema import ForeignKey


class HashEnum(Enum):
    @override
    @staticmethod
    def _generate_next_value_(
            name: str, start: int, 
            count: int, last_values: list[int]
        ) -> int:
        hash = zlib.crc32(name.encode())
        if hash in last_values:
            raise ValueError (f"Error in HashEnum class\n Key {name} generate hash {hash} which is already in use.")
        return hash


class MethodTypes(HashEnum):
    START_POINT = auto() 
    END_OF_STEP = auto() 
    END_OF_GAME = auto()
    NPC_REPLICA = auto()
    PLAYER_REPLICA = auto()


class Base(DeclarativeBase): pass


class EventMethodDict(Base):
    __tablename__: str = "event_method_dict"

    method_id: Mapped[MethodTypes] = mapped_column(primary_key=True)
    method_name: Mapped[str] = mapped_column()

    @classmethod
    def setUp(cls, session: Session):
        ...


class ContentRegistry(Base):
    __tablename__: str = "content_registry";
 
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class NPCDialogContent(Base):
    __tablename__: str = "npc_dialog_content"

    id: Mapped[int] = mapped_column(
        ForeignKey("content_registry.id", onupdate="CASCADE"), 
        primary_key=True
    )
    text: Mapped[str] = mapped_column() 


class PlayerDialogContent(Base):
    __tablename__: str = "player_dialog_content"

    id: Mapped[int] = mapped_column(
        ForeignKey("content_registry.id", onupdate="CASCADE"), 
        primary_key=True
    )
    text: Mapped[str] = mapped_column()


class GameNode(Base):
    __tablename__: str = "game_nodes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    method: Mapped[MethodTypes] = mapped_column(
        ForeignKey("event_method_dict.method_id", onupdate="CASCADE")
    )
    data_id: Mapped[int | None] = mapped_column(
        ForeignKey("content_registry.id", onupdate="CASCADE")
    ) 


class GameGraph(Base):
    __tablename__: str = "game_graph"

    src_id: Mapped[int] = mapped_column(
        ForeignKey("game_nodes.id", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True
    )
    tgt_id: Mapped[int] = mapped_column(
        ForeignKey("game_nodes.id", ondelete="CASCADE", onupdate="CASCADE"), 
        primary_key=True
    )


db_url = "sqlite:///database/db.db"
sql_engine = create_engine(db_url, echo=True)

Base.metadata.create_all(bind=sql_engine)
session = Session(sql_engine)

EventMethodDict.setUp(session)
