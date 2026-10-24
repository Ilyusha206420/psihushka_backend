from app.models import Base

from app.core.database import db_engine
from app.core.constants import Methods

if __name__ == "__main__":
    Base.metadata.create_all(bind=db_engine)
    for met in Methods:
        print(met.name, met.value)
    

    
    print("OK")
