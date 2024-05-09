from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from microservicios.services.texto_waterMark_detector import detectar_texto
from sql_app.dependencias import get_db
from sql_app.models import Image, ImageTagAssociation, Tags

router = APIRouter(prefix="/microservicios")


@router.get("/texto_marcaAgua_detector/detectar_texto/{id}", status_code=200)
def detectar_texto_img(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    image_tag_association = db.query(ImageTagAssociation).filter(
        ImageTagAssociation.image_id == id).first()

    if image_tag_association and image_tag_association.detected == True:
        return {"message": "el procesamiento de deteccion de textos y marcas de agua ya ha sido realizado sobre esa imagen"}

    path = image.path
    texto_detectados = detectar_texto(path)

    if texto_detectados:
        servicio_realizado = db.query(Tags).filter(
            Tags.tag_service == "Text_waterMark_detected").first()
        new_image_tag_association = ImageTagAssociation(
            image_id=id, tags_id=servicio_realizado.id, detected=True)

        db.add(new_image_tag_association)
        db.commit()

        return {"message": "Deteccion de textos y marcas de agua realizada exitosamente"}

    else:
        servicio_realizado = db.query(Tags).filter(
            Tags.tag_service == "Text_waterMark_detected").first()
        new_image_tag_association = ImageTagAssociation(
            image_id=id, tags_id=servicio_realizado.id, detected=False)

        db.add(image)
        db.commit()

        return {f"message": "No se detectaron textos en la imagen"}
