from fastapi import FastAPI
from microservicios.routers import email_detector_router, url_detector_router, static
from sql_app.database import engine, Base

Base.metadata.create_all(bind=engine)

#! Aplicacion FastAPI
app = FastAPI()
app.title = "ATIBO - Scanner de imagenes - Documentación"
app.version = "0.0.1"


@app.get("/", tags=["Home"])
def root_index():
    return {"Bienvenido": "Ingresar a http://127.0.0.1:8000/docs para acceder a la documentación de la API"}


app.include_router(static.router)
app.include_router(email_detector_router.router)
app.include_router(url_detector_router.router)
