# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Make sure to set DATABASE_URL in your environment or in docker-compose.yml
DATABASE_URL = os.getenv("DATABASE_URL") #"postgresql://postgres:postgres@localhost:5432/scheduler_db" 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
