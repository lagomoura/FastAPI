from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON

from .database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    path = Column(String, unique=True, nullable=False, index=True)
    detectado = Column(Boolean, default=False)
    tags = Column(JSON, nullable=True)
    
    def __init__(self, path:str, detectado:bool, tags:list = []):
        self.path = path
        self.detectado = detectado
        self.tags = tags if tags is not None else []
    
    #! uuid - ver tema id