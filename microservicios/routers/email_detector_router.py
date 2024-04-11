
# . Controler - Direcciona endpoint al archivo
from typing import List, Optional  # define tipos de datos
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field  # Manejo de herencia
from sqlalchemy.orm import Session
from sql_app.dependencias import get_db
from sql_app.models import Image
from fastapi import File, UploadFile
from microservicios.services.email_detector import email_detector

#! Enrutador llamado router con un prefijo de URL "/microservicios/email_detector" para manejar los endpoints relacionados al microservicios
router = APIRouter(prefix="/microservicios/email_detector")

#! Define una clase DetectarEmailImg_Response que hereda de BaseModel, la cual define la estructura de la respuesta para la detección del email en img
class DetectarEmailImg_Request(BaseModel):
    path: str  # path del imagen
    tags: list = Field(default_factory=list)

#! Define un campo file_name de tipo str en la clase DetectarEmailImg_Request para almacenar el nombre del archivo de imagen.
class DetectarEmailImg_Response(BaseModel):
    id: int
    path: str
    tags: list = Field(default_factory=list)
    detectado: Optional[bool]

#! Indica que el método manejará las solicitudes GET en la ruta "/" del enrutador. La respuesta de este endpoint será una lista de objetos de tipo DetectarEmailImg_Response.  
@router.get("/{id}", response_model=List[DetectarEmailImg_Response], status_code=200)
def obtener_image(id:int, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == id).first()
    if image:
        #Obteniendo informacion de la imagen y sus etiquetas
        path = image.path
        detectado = email_detector(path)
        
        return DetectarEmailImg_Response(
            id = image.id,
            path = image.path,
            tags = image.tags,
            detectado = detectado
        )
    
    else:
        raise HTTPException(status_code=404, detail="Imagen no encontrada") 
    

#! Maneja las solicitudes POST en la ruta "/" del enrutador. El parámetro response_model especifica que la respuesta de este endpoint será un objeto de tipo DetectarEmailImg_Response, y devolverá un código de estado HTTP 201 (Created) en la respuesta.
@router.post("/upload", response_model=DetectarEmailImg_Response, status_code=201)
def cargar_img(file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    with open(f"src/imgs/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
        db_img = Image(path=f"src/imgs/{file.filename}", detectado=False, tags=[])
        db.add(db_img)
        db.commit()

    return DetectarEmailImg_Response(id=db_img.id, path=db_img.path, tags=db_img.tags, detectado=db_img.detectado)       

@router.get("/detectar_email/{id}", status_code=200)
def detectar_email_img(id:int, db:Session = Depends(get_db)):
    
    image = db.query(Image).filter(Image.id == id).first()
    
    if image:
        path = image.path
        email_detectados = email_detector(path)
    
        if email_detectados:
            
            if "email_detected" not in image.tags:
            
            #todo si email_detected no existe en el array tags, corro el detector de email - Mantener los tags existentes
            #todo guardar en columna las pruebas que ya fueron procesadas a cada imagen
            
                email_tag = "email_detected"
                image.detectado = True
                image.tags = email_tag
                db.add(image)
                db.commit()
    
                return {"message":"Deteccion de emails realizada exitosamente"}
            else:
                return {"message":"el procesamiento de deteccion de emails ya ha sido realizado sobre esa imagen"}
        else:
            return {f"message": "No se detectaron emails en la imagen"}
    else:
        raise HTTPException(status_code=404, detail="Image no encontrada")
