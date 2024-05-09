from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from microservicios.services.url_detector import url_detector
from sql_app.dependencias import get_db
from sql_app.models import Image, ImageTagAssociation, Tags

router = APIRouter(prefix="/microservicios")


@router.get("/url_detector/detectar_url/{id}", status_code=200)
def detectar_url_img(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    image_tag_association = db.query(ImageTagAssociation).filter(
        ImageTagAssociation.image_id == id).first()

    if image_tag_association and image_tag_association.detected == True and image_tag_association.tags_id == 8:
        return {"message": "el procesamiento de deteccion de URLs ya ha sido realizado sobre esa imagen"}

    path = image.path
    url_detectados = url_detector(path)

    if url_detectados:
        servicio_realizado = db.query(Tags).filter(
            Tags.tag_service == "URL_detected").first()
        new_image_tag_association = ImageTagAssociation(
            image_id=id, tags_id=servicio_realizado.id, detected=True)

        db.add(new_image_tag_association)
        db.commit()

        return {"message": "Deteccion de textos y marcas de agua realizada exitosamente"}

    else:
        servicio_realizado = db.query(Tags).filter(
            Tags.tag_service == "URL_detected").first()
        new_image_tag_association = ImageTagAssociation(
            image_id=id, tags_id=servicio_realizado.id, detected=False)

        db.add(new_image_tag_association)
        db.commit()

        return {f"message": "No se detectaron Urls en la imagen"}
