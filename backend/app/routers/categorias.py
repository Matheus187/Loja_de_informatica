from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from backend.app.database import engine
from pydantic import BaseModel

router = APIRouter()


class CategoriaSchema(BaseModel):
    nome: str

@router.post("/")
def criar_categoria(categoria: CategoriaSchema):
    with engine.begin() as conn:
        try:
            query = text("INSERT INTO categorias (nome) VALUES (:nome) RETURNING id")
            result = conn.execute(query, {"nome": categoria.nome})
            return {"id": result.scalar(), "message": "Categoria criada com sucesso"}
        except Exception as e:
            
            raise HTTPException(status_code=400, detail=f"Erro ao criar categoria: {str(e)}")

@router.get("/")
def listar_categorias():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM categorias")).mappings().fetchall()
        return [dict(row) for row in result]

@router.put("/{id}")
def editar_categoria(id: int, categoria: CategoriaSchema):
    with engine.begin() as conn:
        query = text("UPDATE categorias SET nome = :nome WHERE id = :id")
        result = conn.execute(query, {"nome": categoria.nome, "id": id})
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
        
        return {"message": "Categoria atualizada com sucesso"}

@router.delete("/{id}")
def deletar_categoria(id: int):
    with engine.begin() as conn:
        
        produtos_vinculados = conn.execute(
            text("SELECT 1 FROM produtos WHERE categoria_id = :id LIMIT 1"), 
            {"id": id}
        ).fetchone()
        
        if produtos_vinculados:
            raise HTTPException(
                status_code=400, 
                detail="Não é possível excluir esta categoria pois existem produtos vinculados a ela."
            )

        
        result = conn.execute(text("DELETE FROM categorias WHERE id = :id"), {"id": id})
        
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Categoria não encontrada")
            
        return {"message": "Categoria excluída com sucesso"}