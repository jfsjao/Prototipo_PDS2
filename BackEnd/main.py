from fastapi import FastAPI, status, Depends
import classes
import model
from database import engine, get_db
from sqlalchemy.orm import Session

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "lala"}

@app.get("/quadrado/{num}")
def square(num: int):
    return num ** 2

@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(titulo=nova_mensagem.titulo, conteudo=nova_mensagem.conteudo, publicada=nova_mensagem.publicada)
    db.add(mensagem_criada)
    db.commit()
    return {"Mensagem": mensagem_criada}