from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app.dependencias import get_db
from sql_app.models import Image

from microservicios.services.texto_waterMark_detector import detectar_texto

router = APIRouter(prefix="/microservicios")


@router.get("/texto_marcaAgua_detector/detectar_texto/{id}", status_code=200)
def detectar_texto_img(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()

    if image:
        path = image.path
        texto_detectados = detectar_texto(path)
        service_tag = ["TEXTO_DETECTOR"]

        if "TEXTO_DETECTOR" not in image.services:
            image.services = service_tag

        else:
            return {"message": "el procesamiento de deteccion de textos/marcas de Agua ya ha sido realizado sobre esa imagen"}

        if texto_detectados:
            url_tag = ["TEXTO_detected"]
            image.tags = url_tag

            db.add(image)
            db.commit()

            return {"message": "Deteccion de texto/marca de agua realizada exitosamente"}
        else:
            db.add(image)
            db.commit()
            return {f"message": "No se detectaron textos en la imagen"}
    else:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
