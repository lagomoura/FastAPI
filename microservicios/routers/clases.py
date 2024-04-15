from typing import Optional  # define tipos de datos
from pydantic import BaseModel, Field  # Manejo de herencia


#! Define una clase DetectarEmailImg_Response que hereda de BaseModel, la cual define la estructura de la respuesta para la detección del email en img
class BaseImg_Request(BaseModel):
    tags: list = Field(default_factory=list)
    services: list = Field(default_factory=list)

#! Define un campo file_name de tipo str en la clase BaseImg_Request para almacenar el nombre del archivo de imagen.
class BaseImg_Response(BaseModel):
    id: str
    tags: list = Field(default_factory=list)
    services: Optional[list] = Field(default_factory=list)
    path: str
