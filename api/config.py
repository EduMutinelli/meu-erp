import os

class Config:
    PORT = int(os.getenv("API_PORT", 8001))  # Porta padrão 8001
    HOST = os.getenv("API_HOST", "0.0.0.0")