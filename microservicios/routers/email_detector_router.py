
# . Controler - Direcciona endpoint al archivo
from typing import List  # define tipos de datos
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field  # Manejo de herencia
from sqlalchemy.orm import Session
from sql_app.dependencias import get_db
from sql_app.models import Image
from fastapi import File, UploadFile

#! Enrutador llamado router con un prefijo de URL "/microservicios/email_detector" para manejar los endpoints relacionados al microservicios
router = APIRouter(prefix="/microservicios/email_detector")

#! Define una clase DetectarEmailImg_Response que hereda de BaseModel, la cual define la estructura de la respuesta para la detección del email en img
class DetectarEmailImg_Request(BaseModel):
    path: str  # path del imagen
    status: bool  # Detectado / No detectado
    tags: list = Field(default_factory=list)

#! Define un campo file_name de tipo str en la clase DetectarEmailImg_Request para almacenar el nombre del archivo de imagen.
class DetectarEmailImg_Response(BaseModel):
    id: int
    path: str
    status: bool
    tags: List[str] = Field(default_factory=list)

#! Indica que el método manejará las solicitudes GET en la ruta "/" del enrutador. La respuesta de este endpoint será una lista de objetos de tipo DetectarEmailImg_Response.  
@router.get("/{id}", response_model=List[DetectarEmailImg_Response], status_code=200)
def detectar_email_img(id:int, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == id).first()
    if image:
        #Obteniendo informacion de la imagen y sus etiquetas
        image_data = {
            "Id": image.id,
            "path": image.path,
            "status": image.status,
            "tags": image.tags
        }
        
        return image_data
    
    else:
        {"Imagen no encontrada"}
    

#! Maneja las solicitudes POST en la ruta "/" del enrutador. El parámetro response_model especifica que la respuesta de este endpoint será un objeto de tipo DetectarEmailImg_Response, y devolverá un código de estado HTTP 201 (Created) en la respuesta.
@router.post("/", response_model=DetectarEmailImg_Request, status_code=201)
def cargar_img(file: UploadFile = File(...), db: Session = Depends(get_db)):
    
    #. Guardar img en carpeta
    with open(f"src/imgs/{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
        db_img = Image(path=f"src/imgs/{file.filename}", status=False, tags="[]")
        db.add(db_img)
        db.commit()
            
            #todo ver sistema de cola para la respuesta
    
    return DetectarEmailImg_Response(id=db_img.id, path=db_img.path, status=db_img.status)
