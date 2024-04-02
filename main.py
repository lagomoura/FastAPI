from fastapi import FastAPI
from microservicios.routers import email_detector_router

app = FastAPI()

@app.get("/")
def root_index():
  return {"Test":"Test"}

app.include_router(email_detector_router.router)