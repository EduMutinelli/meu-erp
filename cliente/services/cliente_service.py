from .api_client import APIClient
import streamlit as st

class ClienteService:
    def __init__(self):
        self.api = APIClient()
        self.endpoint = "/clientes"

    def criar_cliente(self, cliente_data):
        return self.api.post("/clientes/", cliente_data)
    
    def listar_clientes(self):
        resultado = self.api.get(self.endpoint)
        if resultado and 'clientes' in resultado:
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
        
        