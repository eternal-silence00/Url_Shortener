from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime, timezone

class Base(DeclarativeBase):
    pass

class Url(Base):
    __tablename__ = "url"
    
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False, unique=True)
    short_code = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
     