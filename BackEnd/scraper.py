import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, MenuNav
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Ler variáveis de ambiente
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
database = os.getenv("DATABASE_NAME")
host = os.getenv("DATABASE_HOST")

# Garantir que todas as variáveis foram carregadas corretamente
if not all([user, password, database, host]):
    raise ValueError("❌ ERRO: Algumas variáveis de ambiente do banco de dados não foram definidas corretamente!")

# Montar URL do banco de dados
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{database}"

# Criar engine de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

# Função para inserir os dados no banco
def insert_data(menu_items):
    db = SessionLocal()
    try:
        for item in menu_items:
            db.add(MenuNav(menuNav=item['menuNav'], link=item['link']))
        db.commit()
    finally:
        db.close()

# Endpoint para disparar o Web Scraping manualmente
def scrape_ufu_data():
    # Realizar o Web Scraping
    menu_items = scrape_ufu()

    # Inserir os dados no banco
    insert_data(menu_items)

    return {"message": f"{len(menu_items)} items foram inseridos no banco."}

# Chamando a função de scraping diretamente
if __name__ == "__main__":
    scrape_ufu_data()  # Executa o scraping e armazena no banco de dados
