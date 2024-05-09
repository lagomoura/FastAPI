
# . Controler - Direcciona endpoint al archivo
from fastapi import APIRouter
from sql_app.dependencias import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app.models import Image, Tags, ImageTagAssociation

from microservicios.services.address_phone_detector import address_phone_detector

router = APIRouter(prefix="/microservicios")


@router.get("/address_phone_detector/address_phone_detector{id}", status_code=200)
def detector_direccion_telefono(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()
    if not image:
    
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
    
    
    image_tag_association = db.query(ImageTagAssociation).filter(ImageTagAssociation.image_id == id).first()
    
    if image_tag_association and image_tag_association.detected == True:
        
        return {"message": " El procesamiento de deteccion de direcciones y telefonos ya ha sido realizado sobre esa imagen"}
        
        
    path = image.path
    address_phone_detectados = address_phone_detector(path)
    
    if address_phone_detectados:
        
        servicio_realizado = db.query(Tags).filter(Tags.tag_service == "Address_phone_detected").first()
        new_image_tag_association = ImageTagAssociation(image_id = id, tags_id = servicio_realizado.id, detected = True)
        db.add(new_image_tag_association)
        db.commit()
    
        return {"message": "Deteccion de direcciones y telefonos realizada exitosamente"}
    
    else:
        servicio_realizado = db.query(Tags).filter(Tags.tag_service == "Address_phone_detected").first()    
        new_image_tag_association = ImageTagAssociation(image_id = id, tags_id = servicio_realizado.id, detected = False)
        db.add(new_image_tag_association)
        db.commit()
        
        return {"message": "No ha sido detectado direcciones y/o nums. telelefonos en la imagen"}
