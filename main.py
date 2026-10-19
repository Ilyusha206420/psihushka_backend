from fastapi import FastAPI, Response, HTTPException
from uuid import uuid4
from pydantic import BaseModel
from enum import StrEnum
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.schema import ForeignKey

class MethodTypes(StrEnum):
    START_POINT = "START_POINT"
    END_OF_STEP = "END_OF_STEP"
    END_OF_GAME = "END_OF_GAME"
    NPC_REPLICA = "NPC_REPLICA"
    PLAYER_REPLICA = "PLAYER_REPLICA"

class Base(DeclarativeBase): pass

class EventMethodDict(Base):
    __tablename__: str = "event_method_dict"
    methhod_id: Mapped[MethodTypes] = mapped_column(primary_key=True, autoincrement=True)
    method_name: Mapped[str] = mapped_column()

class ContentRegistry(Base):
    __tablename__: str = "content_registry";
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

class NPCDialogContent(Base):
    __tablename__: str = "npc_dialog_content"
    id: Mapped[int] = mapped_column(ForeignKey("content_registry.id"), primary_key=True)
    text: Mapped[str] = mapped_column() 

class PlayerDialogContent(Base):
    __tablename__: str = "player_dialog_content"
    id: Mapped[int] = mapped_column(ForeignKey("content_registry.id"), primary_key=True)
    text: Mapped[str] = mapped_column()

db_url = "sqlite:///database/db.db"
sql_engine = create_engine(db_url, echo=True)

class sessionCookie(BaseModel):
    cookie: str

app = FastAPI()

@app.get("/new_session")
async def new_session(response: Response):
    response.set_cookie(key="session_cookie", value=uuid4().hex)

    return HTTPException(status_code=201)

@app.post("/game_step")
def game_step(session_cookie: sessionCookie):
    session_cookie.cookie
