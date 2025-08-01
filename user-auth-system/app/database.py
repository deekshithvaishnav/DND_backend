from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

#Configure your database URL (change username, password, db name as needed)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345678@localhost:2424/tool_db"

#Engine is the actual connection to DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 🔄 SessionLocal: used for DB transactions per request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 📐 Base class for all models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db  # give the session to the route
    finally:
        db.close()  # close it after the request is done