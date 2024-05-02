from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app.dependencias import get_db
from sql_app.models import Image

from microservicios.services.qr_detector import qr_detector

router = APIRouter(prefix="/microservicios")


@router.get("/qr_detector/detectar_qr/{id}", status_code=200)
def detectar_qr_img(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()

    if image:
        path = image.path
        qr_detectado = qr_detector(path)
        service_tag = ["QR_DETECTOR"]

        if "QR_DETECTOR" not in image.services:
            image.services = service_tag

        else:
            return {"message": "el procesamiento de deteccion de QRs ya ha sido realizado sobre esa imagen"}

        if qr_detectado:
            qr_tag = ["QR_detected"]
            image.tags = qr_tag

            db.add(image)
            db.commit()

            return {"message": "Deteccion de QRs realizada exitosamente - La nueva imagen con QR en blur ha sido guardada en carpeta local"}
        else:
            db.add(image)
            db.commit()
            return {f"message": "No se detectaron QRs en la imagen"}
    else:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
