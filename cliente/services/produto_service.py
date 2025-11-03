# ARQUIVO: cliente/services/produto_service.py

from .api_client import APIClient

class ProdutoService:
    def __init__(self):
        self.api = APIClient()
    
    def criar_produto(self, produto_data):
        return self.api.post("/produtos/", produto_data)
    
    def listar_produtos(self):
        response = self.api.get("/produtos/")
        print(f"🔍 [PRODUTO SERVICE] Resposta da API: {response}")  # Debug
        # ✅ CORREÇÃO: A API retorna {"produtos": [...]}
        if response and "produtos" in response:
            produtos = response["produtos"]
            return produtos if isinstance(produtos, list) else []
        return []
    
    def buscar_produto(self, produto_id):
        response = self.api.get(f"/produtos/{produto_id}")
        return response.get("produto") if response else None
    
    def atualizar_produto(self, produto_id, produto_data):
        return self.api.put(f"/produtos/{produto_id}", produto_data)
    
    def excluir_produto(self, produto_id):
        return self.api.delete(f"/produtos/{produto_id}")