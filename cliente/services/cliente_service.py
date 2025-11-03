from .api_client import APIClient
import streamlit as st

class ClienteService:
    def __init__(self):
        self.api = APIClient()
        self.endpoint = "/clientes"

    def criar_cliente(self, cliente_data):
        return self.api.post("/clientes/", cliente_data)
    
    def listar_clientes(self):
        st.write("🔍 [DEBUG] Chamando API para listar clientes...")
        resultado = self.api.get(self.endpoint)
        st.write(f"🔍 [DEBUG] Resposta da API: {resultado}")
        
        if resultado and 'clientes' in resultado:
            st.success(f"✅ Encontrados {len(resultado['clientes'])} clientes na API")
            return resultado['clientes']
        else:
            st.error("❌ Nenhum cliente retornado da API")
            return []
        
    def buscar_cliente(self, cliente_id):
        response = self.api.get(f"/clientes/{cliente_id}")
        return response.get("cliente") if response else None
    
    def atualizar_cliente(self, cliente_id, cliente_data):
        return self.api.put(f"/clientes/{cliente_id}", cliente_data)
    
    def excluir_cliente(self, cliente_id):
        return self.api.delete(f"/clientes/{cliente_id}")
        
        