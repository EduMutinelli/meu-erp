from .api_client import APIClient
import streamlit as st

class ProdutoService:
    def __init__(self):
        self.api = APIClient()
    
    def listar_produtos(self):
        try:
            resultado = self.api.get("/produtos/")
            
            # Se a API não respondeu
            if resultado is None:
                st.error("❌ API não disponível. Verifique se o servidor está online.")
                return []
            
            # Se a API retornou um dicionário com 'produtos'
            if isinstance(resultado, dict) and 'produtos' in resultado:
                produtos = resultado['produtos']
                if produtos:
                    return produtos
                else:
                    return []  # Lista vazia é normal quando não há produtos
            else:
                # Resposta inesperada
                st.error(f"❌ Resposta inesperada da API: {resultado}")
                return []
                
        except Exception as e:
            st.error(f"❌ Erro ao conectar com a API: {str(e)}")
            return []
    
    def criar_produto(self, produto_data):
        return self.api.post("/produtos/", produto_data)
    
    def buscar_produto(self, produto_id):
        response = self.api.get(f"/produtos/{produto_id}")
        return response.get("produto") if response else None
    
    def atualizar_produto(self, produto_id, produto_data):
        try:
            st.write("🔍 Debug - Dados enviados para API:", produto_data)
            resultado = self.api.put(f"/produtos/{produto_id}", produto_data)
            st.write("🔍 Debug - Resposta da API:", resultado)
            return resultado
        except Exception as e:
            st.error(f"❌ Erro ao atualizar produto: {e}")
            return None
    
    def excluir_produto(self, produto_id):
        return self.api.delete(f"/produtos/{produto_id}")