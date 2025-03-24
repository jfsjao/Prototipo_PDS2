from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

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

# Criar sessão do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definir modelo para os dados coletados pelo scraper
class MenuNav(Base):
    __tablename__ = 'menu_nav'
    id = Column(Integer, primary_key=True, index=True)
    menuNav = Column(String, index=True)
    link = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

# Criar a tabela no banco de dados
Base.metadata.create_all(bind=engine)

# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
