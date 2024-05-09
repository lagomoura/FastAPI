from fastapi import FastAPI
from microservicios.routers import email_detector_router, url_detector_router, address_phone_detector_router, texto_marcaAgua_detector_router, human_nsfw_detector_router, qr_detector_router, fondos_transparentes_router

from microservicios.routers.controllers import controller
from sql_app.database import engine, Base


Base.metadata.create_all(bind=engine)

#! Aplicacion FastAPI
app = FastAPI()
app.title = "ATIBO - Scanner de imagenes - Documentación"
app.version = "0.0.1"


@app.get("/", tags=["Home"])
def root_index():
    return {"Bienvenido": "Ingresar a http://127.0.0.1:8000/docs para acceder a la documentación de la API"}


app.include_router(controller.router)
app.include_router(email_detector_router.router)
app.include_router(url_detector_router.router)
app.include_router(address_phone_detector_router.router)
app.include_router(texto_marcaAgua_detector_router.router)
app.include_router(human_nsfw_detector_router.router)
app.include_router(qr_detector_router.router)
app.include_router(fondos_transparentes_router.router)