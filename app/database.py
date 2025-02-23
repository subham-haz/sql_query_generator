from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Read from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://your_db_user:your_db_password@localhost:5432/your_local_db")

# Connect to local PostgreSQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
