from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Image(Base):
    __tablename__ = "Imgs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    path = Column(String, unique=True, nullable=False, index=True)
    status = Column(Boolean, default=False)

    images_tratadas = relationship("Images_Tratadas", back_populates="owner")


class Images_tratadas(Base):
    __tablename__ = "Imgs_Tratadas"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, nullable=False, index=True)
    status = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("Imgs.id"))

    owner = relationship("Image", back_populates="images_tratadas")