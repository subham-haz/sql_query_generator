#model.py
from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(String, nullable=False)
    sql_query = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
