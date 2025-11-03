import pandas as pd
import streamlit as st
from datetime import datetime

# Dados em memória (substitui o banco de dados)
_clientes = []
_produtos = []
_vendas = []

class LocalClienteService:
    def listar_clientes(self):
        return _clientes.copy()
    
    def criar_cliente(self, cliente_data):
        cliente_id = len(_clientes) + 1
        cliente = {
            "id": cliente_id,
            "nome": cliente_data["nome"],
            "email": cliente_data.get("email", ""),
            "telefone": cliente_data.get("telefone", ""),
            "endereco": cliente_data.get("endereco", ""),
            "data_criacao": datetime.now().isoformat()
        }
        _clientes.append(cliente)
        return cliente
    
    def atualizar_cliente(self, cliente_id, cliente_data):
        for cliente in _clientes:
            if cliente["id"] == cliente_id:
                cliente.update({
                    "nome": cliente_data["nome"],
                    "email": cliente_data.get("email", ""),
                    "telefone": cliente_data.get("telefone", ""),
                    "endereco": cliente_data.get("endereco", "")
                })
                return cliente
        return None
    
    def excluir_cliente(self, cliente_id):
        global _clientes
        _clientes = [c for c in _clientes if c["id"] != cliente_id]
        return True

class LocalProdutoService:
    def listar_produtos(self):
        return _produtos.copy()
    
    def criar_produto(self, produto_data):
        produto_id = len(_produtos) + 1
        produto = {
            "id": produto_id,
            "nome": produto_data["nome"],
            "preco": float(produto_data["preco"]),
            "estoque": int(produto_data["estoque"]),
            "categoria": produto_data.get("categoria", ""),
            "descricao": produto_data.get("descricao", ""),
            "data_criacao": datetime.now().isoformat()
        }
        _produtos.append(produto)
        return produto
    
    def atualizar_produto(self, produto_id, produto_data):
        for produto in _produtos:
            if produto["id"] == produto_id:
                produto.update({
                    "nome": produto_data["nome"],
                    "preco": float(produto_data["preco"]),
                    "estoque": int(produto_data["estoque"]),
                    "categoria": produto_data.get("categoria", ""),
                    "descricao": produto_data.get("descricao", "")
                })
                return produto
        return None
    
    def excluir_produto(self, produto_id):
        global _produtos
        _produtos = [p for p in _produtos if p["id"] != produto_id]
        return True

class LocalVendaService:
    def listar_vendas(self):
        return _vendas.copy()
    
    def criar_venda(self, venda_data):
        venda_id = len(_vendas) + 1
        venda = {
            "id": venda_id,
            "cliente_id": venda_data["cliente_id"],
            "produto_id": venda_data["produto_id"],
            "quantidade": int(venda_data["quantidade"]),
            "data_venda": venda_data.get("data_venda", datetime.now().isoformat()),
            "desconto": float(venda_data.get("desconto", 0)),
            "observacoes": venda_data.get("observacoes", ""),
            "valor_total": self._calcular_total(venda_data)
        }
        _vendas.append(venda)
        return venda
    
    def _calcular_total(self, venda_data):
        # Encontra o preço do produto
        for produto in _produtos:
            if produto["id"] == venda_data["produto_id"]:
                preco = produto["preco"]
                quantidade = venda_data["quantidade"]
                desconto = venda_data.get("desconto", 0)
                return (preco * quantidade) - desconto
        return 0