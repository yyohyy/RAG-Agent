from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.config.database import Base

class DocumentMetaData(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    file = Column(String)
    n_chunks = Column(Integer)
    chunker = Column(String)
    embedder = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
