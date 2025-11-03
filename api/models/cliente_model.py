from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Cliente(BaseModel):
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None

class ClienteResponse(Cliente):
    id: int
    data_cadastro: datetime