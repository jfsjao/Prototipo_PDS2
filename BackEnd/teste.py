from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def teste_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API está rodando!"}

def teste_quadrado():
    num = 4
    response = client.get(f"/quadrado/{num}")
    assert response.status_code == 200
    assert response.json() == {"resultado": num ** 2}
