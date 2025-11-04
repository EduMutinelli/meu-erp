

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.clientes import router as clientes_router
from routes.produtos import router as produtos_router  
from routes.vendas import router as vendas_router

app = FastAPI(title="ERP API", version="1.0.0")

# CORS para permitir conexão do Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("🟢 ROTAS REGISTRADAS:")
    for route in app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            print(f"   {list(route.methods)} {route.path}")

# Registrar rotas
app.include_router(clientes_router, prefix="/api/v1")
app.include_router(produtos_router, prefix="/api/v1") 
app.include_router(vendas_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "ERP API Online!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ERP API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)