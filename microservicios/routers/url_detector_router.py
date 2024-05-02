from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app.dependencias import get_db
from sql_app.models import Image

from microservicios.services.url_detector import url_detector

router = APIRouter(prefix="/microservicios")


@router.get("/url_detector/detectar_url/{id}", status_code=200)
def detectar_url_img(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()

    if image:
        path = image.path
        url_detectados = url_detector(path)
        service_tag = ["URL_DETECTOR"]

        if "URL_DETECTOR" not in image.services:
            image.services = service_tag

        else:
            return {"message": "el procesamiento de deteccion de urls ya ha sido realizado sobre esa imagen"}

        if url_detectados:
            url_tag = ["URL_detected"]
            image.tags = url_tag

            db.add(image)
            db.commit()

            return {"message": "Deteccion de URLs realizada exitosamente"}
        else:
            db.add(image)
            db.commit()
            return {f"message": "No se detectaron Urls en la imagen"}
    else:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
