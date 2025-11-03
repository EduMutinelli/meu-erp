from .api_client import APIClient
import streamlit as st

class FinanceiroService:
    def __init__(self):
        self.api = APIClient()
    
    def get_metricas(self):
        # Implementar métricas financeiras
        return {
            "faturamento_total": 0,
            "despesas": 0,
            "lucro": 0
        }