from fastapi import FastAPI, HTTPException
from microservicios.routers import email_detector_router
from sql_app.database import engine, Base
from sql_app.models import Image, Images_tratadas


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


#! Aplicacion FastAPI
app = FastAPI()


@app.get("/")
def root_index():
    return {"Test": "Test"}


app.include_router(email_detector_router.router)
