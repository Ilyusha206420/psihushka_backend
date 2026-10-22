from app.models import Base
from app.core.database import db_engine

if __name__ == "__main__":
    Base.metadata.create_all(bind=db_engine)
    print("OK")
