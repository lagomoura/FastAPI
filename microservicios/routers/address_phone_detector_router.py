
# . Controler - Direcciona endpoint al archivo
from fastapi import APIRouter
from sql_app.dependencias import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app.models import Image

from microservicios.services.address_phone_detector import address_phone_detector

router = APIRouter(prefix="/microservicios")


@router.get("/address_phone_detector/address_phone_detector{id}", status_code=200)
def detector_direccion_telefono(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()

    if image:
        path = image.path
        address_phone_detectados = address_phone_detector(path)
        service_tag = ["ADDRESS_PHONE_DETECTOR"]

        if "ADDRESS_PHONE_DETECTOR" not in image.services:
            image.services = service_tag

        else:
            return {"message": " El procesamiento de deteccion de direcciones y telefonos ya ha sido realizado sobre esa imagen"}

        if address_phone_detectados:
            address_phone_tag = ["ADDRESS_PHONE detected"]
            image.tags = address_phone_tag

            db.add(image)
            db.commit()

            return {"message": "Deteccion de direcciones y telefonos realizada exitosamente"}

        else:
            db.add(image)
            db.commit()
            return {"message": "No se detectaron direcciones o telefonos en la imagen"}

    else:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
