import requests
import streamlit as st
import os

class APIClient:
    def __init__(self):
        # Pega a URL da API dos secrets do Streamlit Cloud
        self.base_url = st.secrets.get("API_URL", "http://localhost:8001/api/v1")
    
    def _request(self, method, endpoint, **kwargs):
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.request(method, url, **kwargs)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Erro na API: {response.status_code}")
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("❌ API não disponível. Verifique se a API está online.")
            return None
        except Exception as e:
            st.error(f"❌ Erro de conexão: {e}")
            return None
    
    def get(self, endpoint):
        return self._request("GET", endpoint)
    
    def post(self, endpoint, data):
        return self._request("POST", endpoint, json=data)
    
    def put(self, endpoint, data=None):
        return self._request("PUT", endpoint, json=data)
    
    def delete(self, endpoint):
        return self._request("DELETE", endpoint)