# ARQUIVO: api/routes/vendas.py (VERSÃO SIMPLIFICADA)

from fastapi import APIRouter, HTTPException
from database import Database
from models.venda_model import Venda

router = APIRouter(tags=["Vendas"])
db = Database()

@router.post("/", response_model=dict)
async def criar_venda(venda: Venda):
    try:
        print(f"📝 [API VENDAS] Recebendo venda: {venda.dict()}")
        
        # 1. Verificar se cliente existe
        query_cliente = "SELECT id FROM clientes WHERE id = %s"
        cliente_existe = db.execute_query(query_cliente, (venda.cliente_id,))
        
        if not cliente_existe:
            raise HTTPException(status_code=400, detail="Cliente não encontrado")
        
        # 2. Verificar produtos e calcular total
        total = 0
        for item in venda.itens:
            # Verificar se produto existe e tem estoque
            query_produto = "SELECT nome, estoque FROM produtos WHERE id = %s"
            produto = db.execute_query(query_produto, (item.produto_id,))
            
            if not produto:
                raise HTTPException(status_code=400, detail=f"Produto ID {item.produto_id} não encontrado")
            
            produto_info = produto[0]
            if produto_info['estoque'] < item.quantidade:
                raise HTTPException(status_code=400, detail=f"Estoque insuficiente para {produto_info['nome']}. Disponível: {produto_info['estoque']}")
            
            total += item.quantidade * item.preco_unitario
        
        print(f"💰 [API VENDAS] Total calculado: {total}")
        
        # 3. Inserir venda
        query_venda = """
        INSERT INTO vendas (cliente_id, total, observacao) 
        VALUES (%s, %s, %s)
        RETURNING id
        """
        venda_id = db.execute_query(query_venda, (venda.cliente_id, total, venda.observacao))
        
        if not venda_id:
            raise HTTPException(status_code=500, detail="Falha ao criar venda")
        
        print(f"✅ [API VENDAS] Venda criada com ID: {venda_id}")
        
        # 4. Inserir itens da venda e atualizar estoque
        for item in venda.itens:
            query_item = """
            INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario) 
            VALUES (%s, %s, %s, %s)
            """
            db.execute_query(query_item, (venda_id, item.produto_id, item.quantidade, item.preco_unitario))
            
            # Atualizar estoque
            query_estoque = "UPDATE produtos SET estoque = estoque - %s WHERE id = %s"
            db.execute_query(query_estoque, (item.quantidade, item.produto_id))
            
            print(f"📦 [API VENDAS] Item adicionado: Produto {item.produto_id}, Quantidade {item.quantidade}")
        
        return {"message": "Venda criada com sucesso", "id": venda_id}
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ [API VENDAS] Erro detalhado: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/", response_model=dict)
async def listar_vendas():
    try:
        print("📝 [API VENDAS] Listando vendas...")
        query = """
        SELECT v.*, c.nome as cliente_nome 
        FROM vendas v 
        LEFT JOIN clientes c ON v.cliente_id = c.id 
        ORDER BY v.data_venda DESC
        """
        vendas = db.execute_query(query)
        print(f"🔍 [API VENDAS] Vendas encontradas: {vendas}")
        return {"vendas": vendas if vendas else []}
    except Exception as e:
        print(f"❌ [API VENDAS] Erro ao listar: {e}")
        return {"vendas": []}

@router.get("/{venda_id}/itens", response_model=dict)
async def listar_itens_venda(venda_id: int):
    try:
        query = """
        SELECT iv.*, p.nome as produto_nome 
        FROM itens_venda iv 
        LEFT JOIN produtos p ON iv.produto_id = p.id 
        WHERE iv.venda_id = %s
        """
        itens = db.execute_query(query, (venda_id,))
        return {"itens": itens if itens else []}
    except Exception as e:
        return {"itens": []}