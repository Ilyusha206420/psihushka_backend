from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

class Base(DeclarativeBase):
    pass

db_engine = create_engine(url=settings.database_url, echo=settings.debug)

SessionLocal = sessionmaker(bind=db_engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
