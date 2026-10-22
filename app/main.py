from enum import Enum, auto
from typing import final, override
import zlib

from fastapi import FastAPI, HTTPException
from sqlalchemy import JSON, Integer, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship
from sqlalchemy.schema import ForeignKey

from pydantic import BaseModel

class HashEnum(Enum):
    @override
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[int]
    ) -> int:
        hash = zlib.crc32(name.encode())
        if hash in last_values:
            raise ValueError(
                "Error in HashEnum class\n"
                + f"Key {name} generate hash {hash} which is already in use."
            )
        return hash


class MethodTypes(HashEnum):
    NPC_REPLICA = auto()
    PLAYER_REPLICA = auto()
    START_POS = auto()


class Base(DeclarativeBase):
    pass


class EventMethod(Base):
    __tablename__: str = "event_method_dict"

    method_id: Mapped[MethodTypes] = mapped_column(Integer, primary_key=True)
    method_name: Mapped[str] = mapped_column(unique=True)

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EventMethod):
            return NotImplemented
        return (
            self.method_id == other.method_id and self.method_name == other.method_name
        )

    @classmethod
    def synchWithSourceMethods(cls, session: Session):
        initialized_methods = session.query(EventMethod).all()
        adding_methods: list[EventMethod] = []
        for met in MethodTypes:
            new_method = EventMethod(method_id=met.value, method_name=met.name)
            need_add = True
            for check in initialized_methods:
                if check == new_method:
                    need_add = False
                    break
                if (
                    check.method_id == new_method.method_id
                    and check.method_name != new_method.method_name
                ):
                    raise ValueError(
                        "Error with adding new method in DB\n"
                        + f"Trying to  add id: {new_method.method_id} name: {new_method.method_name}\n"
                        + f"Error with id: {check.method_id} name: {check.method_name}"
                    )
            if need_add:
                adding_methods.append(new_method)

        session.add_all(adding_methods)
        session.commit()


class ContentRegistry(Base):
    __tablename__: str = "content_registry"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TextsContent(Base):
    __tablename__: str = "texts"

    id: Mapped[int] = mapped_column(
        Text, ForeignKey("content_registry.id", onupdate="CASCADE"), primary_key=True
    )
    text: Mapped[str] = mapped_column(unique=True)


class GameNode(Base):
    __tablename__: str = "game_nodes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    method: Mapped[MethodTypes] = mapped_column(
        Integer, ForeignKey("event_method_dict.method_id", onupdate="CASCADE")
    )
    data_id: Mapped[int | None] = mapped_column(
        ForeignKey("content_registry.id", onupdate="CASCADE")
    )

    # next = relationship("game_nodes", back_populates="GameNode")    


class GameGraph(Base):
    __table_name__: str = "game_graph"

    src_id: Mapped[int] = mapped_column(
        ForeignKey("game_nodes.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    tgt_id: Mapped[int] = mapped_column(
        ForeignKey("game_nodes.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )

class DialogStepResponse(BaseModel):
    npc_texts: list[str] | None = None
    player_texts: list[str] | None = None


EventMethod.synchWithSourceMethods(db)

player_node = db.scalar(select(GameNode).where(GameNode.method == MethodTypes.START_POS.value))
if player_node is None:
    raise ValueError("Something went wrong\nCan't set player start position")

app = FastAPI()

@app.get("/")
def root(): 
    return {"message": "ok"}

@app.post("/reset_session")
def reset_session():
    global player_node
    player_node = db.scalar(select(GameNode).filter(GameNode.method == MethodTypes.START_POS.value))
    if player_node is not None:
        return {
            "msg": "player position was reseted",
            "position_id": player_node.id 
        }
    else:
        return HTTPException(status_code=404)

@app.post("/dialog_step")
def dialog_step(choice_id: int):
    ...
