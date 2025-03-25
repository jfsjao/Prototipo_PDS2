from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import requests
from bs4 import BeautifulSoup

# Importando corretamente as classes do `classes.py`
from classes import Mensagem, MenuNavBase
import model
from database import engine, get_db, MenuNav, SessionLocal

# Inicializando o FastAPI
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

# Criar as tabelas no banco de dados
model.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "API está rodando!"}

@app.get("/quadrado/{num}")
def square(num: int):
    return {"resultado": num ** 2}
    
# Função de Web Scraping
def scrape_ufu():
    url = "https://www.ufu.br"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Encontre os links do menu de navegação
        menu_items = soup.find_all('a')  # Ajuste conforme necessário
        data = []

        for item in menu_items:
            link_text = item.get_text(strip=True)
            link_url = item.get('href')

            if link_text and link_url:
                if link_url.startswith('/'):
                    link_url = f"{url}{link_url}"  # Tornar o link absoluto

                data.append({'menuNav': link_text, 'link': link_url})

        return data
    else:
        print(f"Erro ao acessar o site: {response.status_code}")
        return []

# Função para inserir dados no banco de dados
def insert_data(menu_items):
    db = SessionLocal()
    try:
        for item in menu_items:
            db.add(MenuNav(menuNav=item['menuNav'], link=item['link']))
        db.commit()
    finally:
        db.close()

@app.get("/mensagens", response_model=List[Mensagem], status_code=status.HTTP_200_OK)
async def buscar_valores(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
    return mensagens

@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: Mensagem, db: Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(
        titulo=nova_mensagem.titulo,
        conteudo=nova_mensagem.conteudo,
        publicada=nova_mensagem.publicada
    )
    db.add(mensagem_criada)
    db.commit()  # Aqui o erro foi corrigido
    db.refresh(mensagem_criada)  # Atualiza a mensagem com o ID gerado no banco
    return {"Mensagem": mensagem_criada}

# Endpoint para disparar o Web Scraping manualmente
@app.get("/scrape-ufu")
def scrape_ufu_data():
    # Realizar o Web Scraping
    menu_items = scrape_ufu()  # Chama a função de scraping
    
    # Inserir os dados no banco
    insert_data(menu_items)  # Insere os dados no banco

    return {"message": f"{len(menu_items)} items foram inseridos no banco."}


# Endpoint para retornar os itens de menu (do Web Scraping)
@app.get("/menu-nav", response_model=List[MenuNavBase])
async def get_menu_nav(db: Session = Depends(get_db)):
    menu_nav_items = db.query(MenuNav).all()
    return menu_nav_items
