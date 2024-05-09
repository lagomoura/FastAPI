import uuid

from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

#Para cargar los tags, necesito pasar la importacion sin el (.) para correr la app, necesito agregar el (.)
from .database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    path = Column(String, unique=True, nullable=False, index=True)
    
    tags_associated = relationship("ImageTagAssociation", back_populates='image')
    

class Tags(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, nullable=False)
    tag_service = Column(String(255), unique=False, nullable=True)
    
    images_associated = relationship("ImageTagAssociation", back_populates='tag')
    
class ImageTagAssociation(Base):
    __tablename__ = 'image_tag_association'
    
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(String, ForeignKey("images.id"))
    tags_id = Column(Integer, ForeignKey("tags.id"))
    detected = Column(Boolean, nullable= True, default=False)
    
    image = relationship('Image', back_populates='tags_associated')
    tag = relationship("Tags", back_populates='images_associated')