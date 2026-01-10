from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from backend.app.database import engine
from backend.app.schemas import ProdutoCreate 

router = APIRouter()

@router.post("/")
def criar_produto(produto: ProdutoCreate):
    with engine.begin() as conn:
        query = text("""
            INSERT INTO produtos (nome, descricao, preco, estoque, categoria_id)
            VALUES (:nome, :descricao, :preco, :estoque, :categoria_id)
            RETURNING id
        """)
        result = conn.execute(query, {
            "nome": produto.nome,
            "descricao": produto.descricao,
            "preco": produto.preco,
            "estoque": produto.estoque,
            "categoria_id": produto.categoria_id
        })
        return {"id": result.scalar(), "message": "Produto criado com sucesso"}

@router.get("/")
def listar_produtos():
    with engine.connect() as conn:
        query = text("""
            SELECT p.*, c.nome as categoria_nome 
            FROM produtos p
            LEFT JOIN categorias c ON p.categoria_id = c.id
        """)
        result = conn.execute(query).mappings().fetchall()
        return [dict(row) for row in result]

@router.put("/{id}")
def editar_produto(id: int, produto: ProdutoCreate):
    with engine.begin() as conn:
        query = text("""
            UPDATE produtos 
            SET nome = :nome, descricao = :descricao, preco = :preco, 
                estoque = :estoque, categoria_id = :categoria_id
            WHERE id = :id
        """)
        result = conn.execute(query, {
            "id": id,
            "nome": produto.nome,
            "descricao": produto.descricao,
            "preco": produto.preco,
            "estoque": produto.estoque,
            "categoria_id": produto.categoria_id
        })
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return {"message": "Produto atualizado"}

@router.delete("/{id}")
def deletar_produto(id: int):
    with engine.begin() as conn:
        vendas_existentes = conn.execute(
            text("SELECT 1 FROM itens_venda WHERE produto_id = :id LIMIT 1"), {"id": id}
        ).fetchone()
        
        if vendas_existentes:
            raise HTTPException(status_code=400, detail="Não é possível deletar um produto que já possui vendas registradas.")

        result = conn.execute(text("DELETE FROM produtos WHERE id = :id"), {"id": id})
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return {"message": "Produto deletado"}