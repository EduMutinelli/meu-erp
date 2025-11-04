from fastapi import APIRouter, HTTPException
from database import Database
from models.produto_model import Produto

router = APIRouter(tags=["Produtos"])
db = Database()

@router.post("/", response_model=dict)
async def criar_produto(produto: Produto):
    try:
        query = """
        INSERT INTO produtos (nome, preco, estoque, categoria, descricao) 
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """
        result = db.execute_query(query, (
            produto.nome, produto.preco, produto.estoque,
            produto.categoria, produto.descricao
        ))
        
        if result:
            return {"message": "Produto criado com sucesso", "id": result}
        else:
            raise HTTPException(status_code=500, detail="Falha ao criar produto")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/", response_model=dict)
async def listar_produtos():
    try:
        query = "SELECT * FROM produtos ORDER BY data_cadastro DESC"
        produtos = db.execute_query(query)
        return {"produtos": produtos if produtos else []}
    except Exception as e:
        return {"produtos": []}

@router.get("/{produto_id}", response_model=dict)
async def buscar_produto(produto_id: int):
    try:
        query = "SELECT * FROM produtos WHERE id = %s"
        result = db.execute_query(query, (produto_id,))
        if not result:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return {"produto": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{produto_id}", response_model=dict)
async def atualizar_produto(produto_id: int, produto: Produto):
    try:
        query = """
        UPDATE produtos 
        SET nome = %s, preco = %s, estoque = %s, categoria = %s, descricao = %s 
        WHERE id = %s
        """
        result = db.execute_query(query, (
            produto.nome, produto.preco, produto.estoque,
            produto.categoria, produto.descricao, produto_id
        ))
        return {"message": "Produto atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{produto_id}", response_model=dict)
async def excluir_produto(produto_id: int):
    try:
        query = "DELETE FROM produtos WHERE id = %s"
        db.execute_query(query, (produto_id,))
        return {"message": "Produto excluído com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))