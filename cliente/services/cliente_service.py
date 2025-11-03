# ARQUIVO: cliente/services/cliente_service.py

from .api_client import APIClient

class ClienteService:
    def __init__(self):
        self.api = APIClient()
    
    def criar_cliente(self, cliente_data):
        return self.api.post("/clientes/", cliente_data)
    
    def listar_clientes(self):
        response = self.api.get("/clientes/")
        print(f"🔍 [CLIENTE SERVICE] Resposta da API: {response}")  # Debug
        # ✅ CORREÇÃO: A API retorna {"clientes": [...]}
        if response and "clientes" in response:
            clientes = response["clientes"]
            # Garantir que é uma lista
            return clientes if isinstance(clientes, list) else []
        return []  # Retorna lista vazia em caso de erro
    
    def buscar_cliente(self, cliente_id):
        response = self.api.get(f"/clientes/{cliente_id}")
        return response.get("cliente") if response else None
    
    def atualizar_cliente(self, cliente_id, cliente_data):
        return self.api.put(f"/clientes/{cliente_id}", cliente_data)
    
    def excluir_cliente(self, cliente_id):
        return self.api.delete(f"/clientes/{cliente_id}")