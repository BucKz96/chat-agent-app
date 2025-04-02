from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender = Column(String, index=True)
    content = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
