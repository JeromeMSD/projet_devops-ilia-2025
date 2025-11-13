# models.py
from sqlalchemy import Column, Integer, Float, DateTime, String
from .database import Base


class CSPRecord(Base):
    __tablename__ = "csp_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    external_id = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    value = Column(Float)
    status = Column(String, default="raw")  # raw / processed / error
