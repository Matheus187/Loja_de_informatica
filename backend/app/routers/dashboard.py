from fastapi import APIRouter
from sqlalchemy import text
from backend.app.database import engine

router = APIRouter()

@router.get("/resumo")
def obter_resumo_dashboard():
    with engine.connect() as conn:
    
        query_faturamento = text("""
            SELECT COALESCE(SUM(quantidade * preco_unitario), 0) 
            FROM itens_venda
        """)
        faturamento = conn.execute(query_faturamento).scalar()

        query_total_pedidos = text("SELECT COUNT(*) FROM vendas")
        total_pedidos = conn.execute(query_total_pedidos).scalar()

        query_top_produtos = text("""
            SELECT p.nome, SUM(iv.quantidade) as total_vendido
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            GROUP BY p.nome
            ORDER BY total_vendido DESC
            LIMIT 5
        """)
        top_produtos = conn.execute(query_top_produtos).mappings().fetchall()

        query_vendedores = text("""
            SELECT v.nome, COUNT(ve.id) as qtd_vendas
            FROM vendedores v
            LEFT JOIN vendas ve ON v.id = ve.vendedor_id
            GROUP BY v.nome
            ORDER BY qtd_vendas DESC
        """)
        ranking_vendedores = conn.execute(query_vendedores).mappings().fetchall()

        return {
            "metricas_gerais": {
                "faturamento_total": float(faturamento),
                "total_pedidos": total_pedidos
            },
            "top_produtos": [dict(p) for p in top_produtos],
            "ranking_vendedores": [dict(v) for v in ranking_vendedores]
        }