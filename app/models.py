from sqlalchemy import Column, Integer, String, DateTime
from config import Base


class EventStore(Base):
    __tablename__ = 'event_store'

    id = Column(Integer, primary_key=True)
    event = Column(String)
    date = Column(DateTime(timezone=True))
        
