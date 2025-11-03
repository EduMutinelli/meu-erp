# ARQUIVO: api/routes/clientes.py

from fastapi import APIRouter, HTTPException
from database import Database
from models.cliente_model import Cliente

router = APIRouter(prefix="/clientes", tags=["Clientes"])
db = Database()

@router.post("/", response_model=dict)
async def criar_cliente(cliente: Cliente):
    try:
        print(f"📝 [API] Recebendo dados do cliente: {cliente.dict()}")
        
        query = """
        INSERT INTO clientes (nome, email, telefone, endereco) 
        VALUES (%s, %s, %s, %s)
        RETURNING id
        """
        result = db.execute_query(query, (
            cliente.nome, 
            cliente.email, 
            cliente.telefone, 
            cliente.endereco
        ))
        
        print(f"🔍 [API] Resultado do INSERT: {result}")
        
        if result:
            return {"message": "Cliente criado com sucesso", "id": result}
        else:
            raise HTTPException(status_code=500, detail="Falha ao criar cliente no banco")
            
    except Exception as e:
        print(f"❌ [API] Erro detalhado: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/", response_model=dict)
async def listar_clientes():
    try:
        print("📝 [API] Listando clientes...")
        query = "SELECT * FROM clientes ORDER BY data_cadastro DESC"
        clientes = db.execute_query(query)
        print(f"🔍 [API] Clientes encontrados: {clientes}")
        return {"clientes": clientes if clientes else []}
    except Exception as e:
        print(f"❌ [API] Erro ao listar: {e}")
        return {"clientes": []}
    
@router.put("/{cliente_id}", response_model=dict)
async def atualizar_cliente(cliente_id: int, cliente: Cliente):
    try:
        query = """
        UPDATE clientes 
        SET nome = %s, email = %s, telefone = %s, endereco = %s 
        WHERE id = %s
        """
        result = db.execute_query(query, (
            cliente.nome, cliente.email, cliente.telefone, 
            cliente.endereco, cliente_id
        ))
        
        if result is not None:  # UPDATE retorna número de linhas afetadas
            return {"message": "Cliente atualizado com sucesso"}
        else:
            raise HTTPException(status_code=500, detail="Falha ao atualizar cliente")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")