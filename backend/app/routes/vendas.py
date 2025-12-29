from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from backend.app.database import engine
from backend.app.schemas import VendaCreate

app = FastAPI()

@app.post("/vendas/")
def criar_venda(venda: VendaCreate):
    with engine.begin() as conn:
        try:

            query_venda = text("""
                INSERT INTO vendas (cliente_id, vendedor_id, metodo_pagamento)
                VALUES (:cliente_id, :vendedor_id, :metodo_pagamento)
                RETURNING id
            """)
            
            result = conn.execute(query_venda, {
                "cliente_id": venda.cliente_id,
                "vendedor_id": venda.vendedor_id,
                "metodo_pagamento": venda.metodo_pagamento
            })
            
            nova_venda_id = result.scalar()
            
            for item in venda.itens:                
                query_preco = text("SELECT preco FROM produtos WHERE id = :pid")
                result_preco = conn.execute(query_preco, {"pid": item.produto_id}).fetchone()
                
                if not result_preco:
                    raise HTTPException(status_code=404, detail=f"Produto {item.produto_id} não encontrado")
                
                preco_atual = result_preco.preco
                
                query_item = text("""
                    INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario)
                    VALUES (:venda_id, :produto_id, :quantidade, :preco)
                """)
                
                conn.execute(query_item, {
                    "venda_id": nova_venda_id,
                    "produto_id": item.produto_id,
                    "quantidade": item.quantidade,
                    "preco": preco_atual
                })
                
                conn.execute(text("""
                    UPDATE produtos SET estoque = estoque - :qtd WHERE id = :pid
                """), {"qtd": item.quantidade, "pid": item.produto_id})

            return {"message": "Venda realizada com sucesso", "id_venda": nova_venda_id}

        except Exception as e:
            print(f"Erro ao processar venda: {e}")
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/vendas/")
def listar_vendas():
    with engine.connect() as conn:
        query = text("""
            SELECT 
                v.id, 
                v.data, 
                v.metodo_pagamento,
                c.nome as nome_cliente,
                ven.nome as nome_vendedor,
                COALESCE(SUM(iv.quantidade * iv.preco_unitario), 0) as total_venda
            FROM vendas v
            INNER JOIN clientes c ON v.cliente_id = c.id
            INNER JOIN vendedores ven ON v.vendedor_id = ven.id
            LEFT JOIN itens_venda iv ON v.id = iv.venda_id
            GROUP BY v.id, c.nome, ven.nome
            ORDER BY v.data DESC
        """)
        
        result = conn.execute(query).fetchall()
        
        vendas_lista = []
        for row in result:
            vendas_lista.append({
                "id": row.id,
                "data": row.data,
                "metodo_pagamento": row.metodo_pagamento,
                "cliente": row.nome_cliente,
                "vendedor": row.nome_vendedor,
                "total": float(row.total_venda) 
            })
            
        return vendas_lista
    
@app.get("/vendas/{id_venda}")
def obter_venda_detalhada(id_venda: int):
    with engine.connect() as conn:

        query_venda = text("""
            SELECT 
                v.id, v.data, v.metodo_pagamento,
                c.nome as cliente_nome, c.telefone as cliente_fone,
                ven.nome as vendedor_nome
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN vendedores ven ON v.vendedor_id = ven.id
            WHERE v.id = :id
        """)
        
        venda = conn.execute(query_venda, {"id": id_venda}).mappings().fetchone()
        
        if not venda:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        query_itens = text("""
            SELECT 
                p.nome as produto_nome,
                p.descricao,
                iv.quantidade,
                iv.preco_unitario,
                (iv.quantidade * iv.preco_unitario) as subtotal
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            WHERE iv.venda_id = :id
        """)
        
        itens = conn.execute(query_itens, {"id": id_venda}).mappings().fetchall()
        
        resultado = dict(venda) 
        resultado["itens"] = [dict(item) for item in itens] 
        resultado["total_geral"] = sum(item["subtotal"] for item in resultado["itens"])
        
        return resultado
    

@app.get("/vendas/{id_venda}")
def obter_venda_detalhada(id_venda: int):
    with engine.connect() as conn:
        query_venda = text("""
            SELECT 
                v.id, v.data, v.metodo_pagamento,
                c.nome as cliente_nome, c.telefone as cliente_fone,
                ven.nome as vendedor_nome
            FROM vendas v
            JOIN clientes c ON v.cliente_id = c.id
            JOIN vendedores ven ON v.vendedor_id = ven.id
            WHERE v.id = :id
        """)
        
        venda = conn.execute(query_venda, {"id": id_venda}).mappings().fetchone()
        
        if not venda:
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        
        query_itens = text("""
            SELECT 
                p.nome as produto_nome,
                p.descricao,
                iv.quantidade,
                iv.preco_unitario,
                (iv.quantidade * iv.preco_unitario) as subtotal
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            WHERE iv.venda_id = :id
        """)
        
        itens = conn.execute(query_itens, {"id": id_venda}).mappings().fetchall()
        
        resultado = dict(venda) 
        resultado["itens"] = [dict(item) for item in itens] 
        resultado["total_geral"] = sum(item["subtotal"] for item in resultado["itens"])
        
        return resultado