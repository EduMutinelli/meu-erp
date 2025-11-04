# ARQUIVO: cliente/services/venda_service.py

from .api_client import APIClient

class VendaService:
    def __init__(self):
        self.api = APIClient()
    
    def criar_venda(self, venda_data):
        return self.api.post("/vendas/", venda_data)
    
    def listar_vendas(self):
        resultado = self.api.get("/vendas/")
        if resultado and 'vendas' in resultado:
            return resultado['vendas']
        else:
            return []
    
    def listar_itens_venda(self, venda_id):
        response = self.api.get(f"/vendas/{venda_id}/itens")
        if response and "itens" in response:
            itens = response["itens"]
            return itens if isinstance(itens, list) else []
        return []