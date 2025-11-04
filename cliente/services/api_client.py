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
            st.write(f"🔍 Debug COMPLETO - API Client:")
            st.write(f"   Base URL: {self.base_url}")
            st.write(f"   Endpoint: {endpoint}")
            st.write(f"   URL Final: {method} {url}")
            st.write(f"   Headers: {kwargs.get('headers', {})}")
            
            response = requests.request(method, url, **kwargs)
            
            st.write(f"🔍 Debug RESPONSE:")
            st.write(f"   Status Code: {response.status_code}")
            st.write(f"   Response Text: {response.text}")
            st.write(f"   Response Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Erro na API: {response.status_code} - {response.text}")
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
    
    def put(self, endpoint, data):
        return self._request("PUT", endpoint, json=data)
    
    def delete(self, endpoint):
        return self._request("DELETE", endpoint)