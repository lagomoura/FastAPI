from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from microservicios.services.fondos_transparentes import quitar_fondos
from sql_app.dependencias import get_db
from sql_app.models import Image, ImageTagAssociation, Tags

router = APIRouter(prefix="/microservicios")


@router.get("/fondo_detector/quitar_fondo/{id}", status_code=200)
def quitar_fondo_img(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()

    if not image:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    image_tag_associatin = db.query(ImageTagAssociation).filter(
        ImageTagAssociation.image_id == id).first()

    if image_tag_associatin and image_tag_associatin.detected == True:
        return {"message": "el procesamiento de remocion de background ya ha sido realizado sobre esa imagen"}

    path = image.path
    fondo_quitado = quitar_fondos(path)

    if fondo_quitado:
        servicio_realizado = db.query(Tags).filter(
            Tags.tag_service == "BG_removed").first()
        new_image_tag_association = ImageTagAssociation(
            image_id=id, tags_id=servicio_realizado.id, detected=True)

        db.add(new_image_tag_association)
        db.commit()

        return {"message": "Background removido exitosamente - La nueva imagen con BG transparente ha sido guardada en carpeta local"}
    else:
        return {"message": "Tuvimos problemas en remover el bg de la imagen"}
