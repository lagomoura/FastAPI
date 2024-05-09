from ..Models.models import BaseImg_Response
from sql_app.models import Image
from fastapi import File, UploadFile
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sql_app.dependencias import get_db
from fastapi import APIRouter

router = APIRouter(prefix = "/static")

#! Indica que el método manejará las solicitudes GET en la ruta "/" del enrutador. La respuesta de este endpoint será una lista de objetos de tipo DetectarEmailImg_Response.  
@router.get("/{id}", response_model=BaseImg_Response, status_code=200)
def obtener_info_image(id:str, db: Session = Depends(get_db)):
    
    image = db.query(Image).filter(Image.id == id).first()
    if image:
        
        return BaseImg_Response(
            id = image.id,
            path = image.path
        )
    
    else:
        raise HTTPException(status_code=404, detail="Imagen no encontrada") 
    

#! Maneja las solicitudes POST en la ruta "/" del enrutador. El parámetro response_model especifica que la respuesta de este endpoint será un objeto de tipo DetectarEmailImg_Response, y devolverá un código de estado HTTP 201 (Created) en la respuesta.
@router.post("/upload", response_model=BaseImg_Response, status_code=201)
def cargar_img(file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    with open(f"src/imgs/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
        db_img = Image(id=str(uuid.uuid4()), path=f"src/imgs/{file.filename}")
        db.add(db_img)
        db.commit()

    return BaseImg_Response(id=db_img.id, path=db_img.path)       