
#. Controler - Direcciona endpoint al archivo

from fastapi import APIRouter
from pydantic import BaseModel  # Manejo de herencia
from typing import List  # define tipos de datos

#! Enrutador llamado router con un prefijo de URL "/microservicios/email_detector" para manejar los endpoints relacionados al microservicios
router = APIRouter(prefix="/microservicios/email_detector")

#! Define una clase DetectarEmailImg_Response que hereda de BaseModel, la cual define la estructura de la respuesta para la detección de correo electrónico en una imagen.
class DetectarEmailImg_Response(BaseModel):
    file_name: str  # nombre img
    path: str  # path del imagen
    status: bool  # Detectado / No detectado

#! Define un campo file_name de tipo str en la clase DetectarEmailImg_Response para almacenar el nombre del archivo de imagen.
class DetectarEmailImg_Request(BaseModel):
    path: str  # path del imagen

#! Indica que el método manejará las solicitudes GET en la ruta "/" del enrutador. La respuesta de este endpoint será una lista de objetos de tipo DetectarEmailImg_Response.
@router.get("/", response_model=List[DetectarEmailImg_Response])
def detectar_email_img():
    return [
        DetectarEmailImg_Response(
            image="img_name",
            path="img_path",
            status=True
        )
    ]

#! Maneja las solicitudes POST en la ruta "/" del enrutador. El parámetro response_model especifica que la respuesta de este endpoint será un objeto de tipo DetectarEmailImg_Response, y status_code=201 indica que se devolverá un código de estado HTTP 201 (Created) en la respuesta.
@router.post("/", response_model=DetectarEmailImg_Response, status_code=201)
def cargar_img(image: DetectarEmailImg_Response):
    return DetectarEmailImg_Response(
            file_name=image.file_name,
            path=image.path,
            status=image.status  # Detectado / No detectado
        )
