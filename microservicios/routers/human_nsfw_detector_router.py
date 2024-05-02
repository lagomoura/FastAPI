# . Controler - Direcciona endpoint al archivo
from fastapi import APIRouter
from sql_app.dependencias import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app.models import Image

from microservicios.services.human_nsfw_detector import detectar_humano

#! Enrutador llamado router con un prefijo de URL "/microservicios
router = APIRouter(prefix="/microservicios")


@router.get("/humano_nsfw_detector/detectar_humano/{id}", status_code=200)
def detectar_humano_nsfw_img(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()

    if image:
        path = image.path
        es_humano, nsfw = detectar_humano(path)
        service_tag = ["HUMANO_NSFW_DETECTOR"]

        if "HUMANO_NSFW_DETECTOR" not in image.services:
            image.services = service_tag

        else:
            return {"message": "El procesamiento de deteccion de humanos y NSFW ya ha sido realizado sobre esa imagen"}

        if es_humano and nsfw:
            humano_tag = ["HUMANO_&_NSFW_detected"]
            image.tags = humano_tag

            db.add(image)
            db.commit()
            return {"message": "Deteccion de Humanos&NSFW realizada exitosamente"}

        elif es_humano and not nsfw:
            humano_tag = ["HUMANO_detected"]
            image.tags = humano_tag
            db.add(image)
            db.commit()
            return {"message": "Deteccion de Huamnos realizada exitosamente. Sin contenido NSFW"}

        elif es_humano == False and nsfw == False:
            db.add(image)
            db.commit()
            return {"message": "No se ha detectado humanos"}

    else:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
