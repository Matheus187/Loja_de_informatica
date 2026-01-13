from fastapi import APIRouter
from sqlalchemy import text
from backend.app.database import engine

router = APIRouter()

@router.get("/categoria-mais-vendida")
def categoria_mais_vendida():
    with engine.connect() as conn:
        query = text("""
            SELECT 
                c.nome AS categoria, 
                COUNT(iv.venda_id) AS total_vendas
            FROM categorias c
            INNER JOIN produtos p ON c.id = p.categoria_id
            INNER JOIN itens_venda iv ON p.id = iv.produto_id
            GROUP BY c.id, c.nome
            ORDER BY total_vendas DESC
            LIMIT 1
        """)
        result = conn.execute(query).mappings().fetchone()
        return dict(result) if result else {"message": "Nenhum dado encontrado"}

@router.get("/categoria-com-mais-produtos")
def categoria_mais_produtos():
    with engine.connect() as conn:
        query = text("""
            SELECT
                c.nome AS categoria,
                COUNT(p.id) as total_produtos
            FROM categorias c
            INNER JOIN produtos p ON c.id = p.categoria_id
            GROUP BY c.id, c.nome
            ORDER BY total_produtos DESC
            LIMIT 1
        """)
        result = conn.execute(query).mappings().fetchone()
        return dict(result) if result else {"message": "Nenhum dado encontrado"}


@router.get("/historico-geral")
def historico_geral():
    with engine.connect() as conn:
        
        query = text("""
            SELECT 
                v.id as venda_id,
                v.data, 
                v.metodo_pagamento, 
                p.nome as produto,
                iv.preco_unitario as valor_venda,
                iv.quantidade,
                c.nome as cliente, 
                ve.nome as vendedor
            FROM vendas v
            JOIN itens_venda iv ON v.id = iv.venda_id
            JOIN produtos p ON iv.produto_id = p.id
            JOIN clientes c ON v.cliente_id = c.id
            JOIN vendedores ve ON v.vendedor_id = ve.id
            ORDER BY v.data DESC
        """)
        result = conn.execute(query).mappings().fetchall()
        return [dict(row) for row in result]