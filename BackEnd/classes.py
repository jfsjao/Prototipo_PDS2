from pydantic import BaseModel

# Modelo Pydantic para a Mensagem
class Mensagem(BaseModel):
    titulo: str
    conteudo: str
    publicada: bool

    class Config:
        from_attributes = True  # Usando 'from_attributes' no Pydantic v2


# Modelo Pydantic para o Menu de Navegação (do Web Scraping)
class MenuNavBase(BaseModel):
    menuNav: str
    link: str

    class Config:
        from_attributes = True  # Usando 'from_attributes' no Pydantic v2
