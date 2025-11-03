from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ItemVenda(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float

class Venda(BaseModel):
    cliente_id: int
    itens: List[ItemVenda]
    observacao: Optional[str] = None

class VendaResponse(Venda):
    id: int
    data_venda: datetime
    total: float