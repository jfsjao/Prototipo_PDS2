from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import classes
import model
from database import engine, get_db

app = FastAPI()

# Permitir chamadas do React
origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Criar tabelas no banco de dados
model.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API está rodando!"}

@app.get("/quadrado/{num}")
def square(num: int):
    return {"resultado": num ** 2}


@app.get("/mensagens", response_model=List[classes.Mensagem], status_code=status.HTTP_200_OK)
async def buscar_valores(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
    return mensagens

@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(
        titulo=nova_mensagem.titulo,
        conteudo=nova_mensagem.conteudo,
        publicada=nova_mensagem.publicada
    )
    db.add(mensagem_criada)
    db.commit()  # Aqui o erro foi corrigido
    db.refresh(mensagem_criada)  # Atualiza a mensagem com o ID gerado no banco
    return {"Mensagem": mensagem_criada}
