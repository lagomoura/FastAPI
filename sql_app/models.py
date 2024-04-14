from sqlalchemy import Boolean, Column, Integer, String, JSON
import uuid

from .database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    path = Column(String, unique=True, nullable=False, index=True)
    detectado = Column(Boolean, default=False)
    tags = Column(JSON, nullable=True, default=[])
    services = Column(JSON, nullable=True, default=[])
    
    #! uuid - ver tema id