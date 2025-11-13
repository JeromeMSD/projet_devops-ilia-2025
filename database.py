# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./csp_ingestor.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # utile pour SQLite + FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
