from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON

from .database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    path = Column(String, unique=True, nullable=False, index=True)
    status = Column(Boolean, default=False)
    tags = Column(JSON, nullable=True)
    
    def __init__(self, path:str, status:bool, tags:list = None):
        self.path = path
        self.status = status
        self.tags = tags if tags else []
    
    #! uuid - ver tema id