# . Controler - Direcciona endpoint al archivo
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from microservicios.services.human_nsfw_detector import detectar_humano
from sql_app.dependencias import get_db
from sql_app.models import Image, ImageTagAssociation, Tags

#! Enrutador llamado router con un prefijo de URL "/microservicios
router = APIRouter(prefix="/microservicios")


@router.get("/humano_nsfw_detector/detectar_humano/{id}", status_code=200)
def detectar_humano_nsfw_img(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    image_tag_association = db.query(ImageTagAssociation).filter(
        ImageTagAssociation.image_id == id).first()

    if image_tag_association and image_tag_association.detected == True:
        return {"message": "El procesamiento de deteccion de humanos y NSFW ya ha sido realizado sobre esa imagen"}

    path = image.path
    es_humano, nsfw = detectar_humano(path)

    if es_humano and nsfw:
        servicio_realizado = db.query(Tags).filter(
            Tags.tag_service == "Human_&_NSFW_detected").first()
        new_image_tag_association = ImageTagAssociation(
            image_id=id, tags_id=servicio_realizado.id, detected=True)

        db.add(new_image_tag_association)
        db.commit()

        return {"message": "Deteccion de Humanos&NSFW realizada exitosamente"}

    elif es_humano and not nsfw:
        servicio_realizado = db.query(Tags).filter(
            Tags.tag_service == "Human_detected").first()
        new_image_tag_association = ImageTagAssociation(
            image_id=id, tags_id=servicio_realizado.id, detected=True)

        db.add(new_image_tag_association)
        db.commit()

        return {"message": "Deteccion de Humano realizada exitosamente. Sin contenido NSFW"}
    else:
        servicio_realizado = db.query(Tags).filter(
        Tags.tag_service == "Human_detected").first()
        new_image_tag_association = ImageTagAssociation(
            image_id=id, tags_id=servicio_realizado.id, detected=False)

        db.add(new_image_tag_association)
        db.commit()
        return {"message": "No se ha detectado humanos"}
