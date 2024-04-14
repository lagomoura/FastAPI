from sqlalchemy import Boolean, Column, ARRAY, Integer, String, JSON

from .database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    path = Column(String, unique=True, nullable=False, index=True)
    detectado = Column(Boolean, default=False)
    tags = Column(JSON, nullable=True, default=[])
    services = Column(JSON, nullable=True, default=[])
    
    #! uuid - ver tema id