from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from microservicios.services.qr_detector import qr_detector
from sql_app.dependencias import get_db
from sql_app.models import Image, ImageTagAssociation, Tags

router = APIRouter(prefix="/microservicios")


@router.get("/qr_detector/detectar_qr/{id}", status_code=200)
def detectar_qr_img(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    image_tag_association = db.query(ImageTagAssociation).filter(
        ImageTagAssociation.image_id == id).first()

    if image_tag_association and image_tag_association.detected == True:
        return {"message": "el procesamiento de deteccion de QRs ya ha sido realizado sobre esa imagen"}

    path = image.path
    qr_detectado = qr_detector(path)

    if qr_detectado:
        servicio_realizado = db.query(Tags).filter(
            Tags.tag_service == "QR_detected").first()
        new_image_tag_association = ImageTagAssociation(
            image_id=id, tags_id=servicio_realizado.id, detected=True)

        db.add(new_image_tag_association)
        db.commit()

        return {"message": "Deteccion de QRs realizada exitosamente - La nueva imagen con QR en blur ha sido guardada en carpeta local"}

    else:
        servicio_realizado = db.query(Tags).filter(
            Tags.tag_service == "QR_detected").first()
        new_image_tag_association = ImageTagAssociation(
            image_id=id, tags_id=servicio_realizado.id, detected=False)

        db.add(new_image_tag_association)
        db.commit()

        return {f"message": "No se detectaron QRs en la imagen"}
