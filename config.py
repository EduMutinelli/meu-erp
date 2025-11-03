import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).parent

# Configurações do banco de dados (SQLite portável)
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)  # Cria pasta se não existir

DATABASE_PATH = DATA_DIR / "erp_database.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Configurações da API
API_HOST = "0.0.0.0"
API_PORT = 8001
API_URL = f"http://localhost:{API_PORT}"

# Configurações do Frontend
FRONTEND_PORT = 8501
FRONTEND_URL = f"http://localhost:{FRONTEND_PORT}"

# Configurações de Log
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "erp_system.log"