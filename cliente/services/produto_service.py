from .api_client import APIClient
import streamlit as st

class ProdutoService:
    def __init__(self):
        self.api = APIClient()
    
    def criar_produto(self, produto_data):
        return self.api.post("/produtos/", produto_data)
    
    def listar_produtos(self):
        resultado = self.api.get(self.endpoint)
        if resultado and 'produtos' in resultado:
            st.success(f"✅ Encontrados {len(resultado['produtos'])} produtos")
            return resultado['produtos']
        else:
            st.error("❌ Nenhum produto foi encontrado")
            return []
    
    def buscar_produto(self, produto_id):
        response = self.api.get(f"/produtos/{produto_id}")
        return response.get("produto") if response else None
    
    def atualizar_produto(self, produto_id, produto_data):
        return self.api.put(f"/produtos/{produto_id}", produto_data)
    
    def excluir_produto(self, produto_id):
        return self.api.delete(f"/produtos/{produto_id}")