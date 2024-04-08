from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    path = Column(String, unique=True, nullable=False, index=True)
    status = Column(Boolean, default=False)
    #tags = Column(String, nullable=True) crear columna tipo json - array vacio como valor por defecto
    #una sola entidad (uno uno) con status default false y una vez detectado cambiara true
    
    #! uuid - ver tema id