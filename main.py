from fastapi import FastAPI
from microservicios.routers import email_detector_router
from sql_app.database import engine, Base

Base.metadata.create_all(bind=engine)

#! Aplicacion FastAPI
app = FastAPI()

@app.get("/")
def root_index():
    return {"Test": "Test"}


app.include_router(email_detector_router.router)
