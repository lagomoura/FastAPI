
# . Controler - Direcciona endpoint al archivo
from fastapi import APIRouter
from sql_app.dependencias import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app.models import Image

from microservicios.services.email_detector import email_detector

#! Enrutador llamado router con un prefijo de URL "/microservicios
router = APIRouter(prefix="/microservicios")

@router.get("/email_detector/detectar_email/{id}", status_code=200)
def detectar_email_img(id:str, db:Session = Depends(get_db)):
    
    image = db.query(Image).filter(Image.id == id).first()
    
    if image:
        path = image.path
        email_detectados = email_detector(path)
        service_tag = ["EMAIL_DETECTOR"]
        
        if "EMAIL_DETECTOR" not in image.services:
            image.services = service_tag
            
        else:
            return {"message":"El procesamiento de deteccion de emails ya ha sido realizado sobre esa imagen"}
    
        if email_detectados:   
            email_tag = ["EMAIL_detected"]
            image.tags = email_tag
                
            db.add(image)
            db.commit()
    
            return {"message":"Deteccion de emails realizada exitosamente"}
        else:
            db.add(image)
            db.commit()
            return {f"message": "No se detectaron emails en la imagen"}
    else:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
