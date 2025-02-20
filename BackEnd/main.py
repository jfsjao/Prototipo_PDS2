from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "lala"}

@app.post("/criar")
def criar_valores(res: dict = Body(...)):
    print(res)
    return {"Mensagem": f"lala: {res['lala']} lele: {res['lele']}"}