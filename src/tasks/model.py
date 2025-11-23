from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.core.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    status = Column(String(20), nullable=False, default="todo")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)