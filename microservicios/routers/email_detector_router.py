
# . Controler - Direcciona endpoint al archivo
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from microservicios.services.email_detector import email_detector
from sql_app.dependencias import get_db
from sql_app.models import Image, ImageTagAssociation, Tags

#! Enrutador llamado router con un prefijo de URL "/microservicios
router = APIRouter(prefix="/microservicios")


@router.get("/email_detector/detectar_email/{id}", status_code=200)
def detectar_email_img(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    image_tag_association = db.query(ImageTagAssociation).filter(
        ImageTagAssociation.image_id == id).first()

    if image_tag_association and image_tag_association.detected == True:

        return {"message": "El procesamiento de deteccion de emails ya ha sido realizado sobre esa imagen"}

    path = image.path
    email_detectados = email_detector(path)

    if email_detectados:
        servicio_realizado = db.query(Tags).filter(
            Tags.tag_service == "Email_detected").first()
        new_image_tag_association = ImageTagAssociation(
            image_id=id, tags_id=servicio_realizado.id, detected=True)

        db.add(new_image_tag_association)
        db.commit()

        return {"message": "Deteccion de emails realizada exitosamente"}

    else:
        servicio_realizado = db.query(Tags).filter(
        Tags.tag_service == "Email_detected").first()
        new_image_tag_association = ImageTagAssociation(
            image_id=id, tags_id=servicio_realizado.id, detected=False)

        db.add(new_image_tag_association)
        db.commit()
        return {f"message": "No se detectaron emails en la imagen"}
