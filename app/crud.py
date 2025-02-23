# crud.py
from sqlalchemy.orm import Session
from app.models import Query

# Create a new query entry
def create_query(db: Session, user_input: str, sql_query: str, response: str):
    db_query = Query(user_input=user_input, sql_query=sql_query, response=response)
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query

# Get all queries
def get_queries(db: Session):
    return db.query(Query).all()

# Get a query by ID
def get_query(db: Session, query_id: int):
    return db.query(Query).filter(Query.id == query_id).first()
