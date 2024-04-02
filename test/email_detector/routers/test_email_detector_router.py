from fastapi.testclient import TestClient
from main import app

cliente = TestClient(app)


def test_cargar_img():
    response = cliente.get("/microservicios/email_detector") # ! Va el mismo path del prefix del router del microservice

    assert response.status_code == 200 
    assert response.json() == [
        {'file_name': 'img_name',
        'path': 'img_path',
        'status': False}
    ]

def test_detectar_email_img():
  nueva_img = {
    "file_name" : "file_name",
    "path" : "path",
    "status": True
  }
  
  response = cliente.post("/microservicios/email_detector", json=nueva_img)
  assert response.status_code == 201
  
  