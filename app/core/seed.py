from app.models import Node
from app.core import Methods
from sqlalchemy.orm import Session

def seed_data(session: Session):
    insert_nodes: list[Node] = [
        Node(method=Methods.START_POS.value)
    ]
    session.add_all(insert_nodes)
    session.commit()

