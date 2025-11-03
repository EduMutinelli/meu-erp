from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Produto(BaseModel):
    nome: str
    preco: float
    estoque: int = 0
    categoria: Optional[str] = None
    descricao: Optional[str] = None

class ProdutoResponse(Produto):
    id: int
    data_cadastro: datetime