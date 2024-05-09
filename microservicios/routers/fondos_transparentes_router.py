from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app.dependencias import get_db
from sql_app.models import Image

from microservicios.services.fondos_transparentes import quitar_fondos

router = APIRouter(prefix="/microservicios")


@router.get("/fondo_detector/quitar_fondo/{id}", status_code=200)
def quitar_fondo_img(id: str, db: Session = Depends(get_db)):

    image = db.query(Image).filter(Image.id == id).first()

    if image:
        path = image.path
        fondo_quitado = quitar_fondos(path)
        service_tag = ["BG_Remover"]

        if "BG_Remover" not in image.services:
            image.services = service_tag

        #else:
            #return {"message": "el procesamiento de remocion de background ya ha sido realizado sobre esa imagen"}

        if fondo_quitado:
            fondo_tag = ["BG_removido"]
            image.tags = fondo_tag

            db.add(image)
            db.commit()

            return {"message": "Background removido exitosamente - La nueva imagen con BG transparente ha sido guardada en carpeta local"}
    else:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")
