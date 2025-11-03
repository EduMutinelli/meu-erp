# ARQUIVO: cliente/services/api_client.py

import requests
import streamlit as st

class APIClient:
    def __init__(self):
        self.base_url = st.secrets["api_config"]["API_URL"]
        print(f"🔗 [API CLIENT] URL base: {self.base_url}")
    
    def post(self, endpoint, data):
        try:
            print(f"📤 [API CLIENT] POST {endpoint} - Dados: {data}")
            response = requests.post(f"{self.base_url}{endpoint}", json=data)
            response.raise_for_status()
            result = response.json()
            print(f"📥 [API CLIENT] Resposta: {result}")
            return result
        except requests.exceptions.RequestException as e:
            st.error(f"Erro na API: {e}")
            return None
    
    def get(self, endpoint):
        try:
            print(f"📤 [API CLIENT] GET {endpoint}")
            response = requests.get(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            result = response.json()
            print(f"📥 [API CLIENT] Resposta: {result}")
            return result
        except requests.exceptions.RequestException as e:
            st.error(f"Erro na API: {e}")
            return None
    
    def put(self, endpoint, data):
        try:
            print(f"📤 [API CLIENT] PUT {endpoint}")
            response = requests.put(f"{self.base_url}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro na API: {e}")
            return None
    
    def delete(self, endpoint):
        try:
            print(f"📤 [API CLIENT] DELETE {endpoint}")
            response = requests.delete(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro na API: {e}")
            return None