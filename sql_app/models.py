from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    path = Column(String, unique=True, nullable=False, index=True)
    status = Column(Boolean, default=False)

    images_tratadas = relationship("ImagesTratadas", back_populates="owner")


class ImagesTratadas(Base):
    __tablename__ = "images_tratadas"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, nullable=False, index=True)
    status = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("images.id"))

    owner = relationship("Image", back_populates="images_tratadas")