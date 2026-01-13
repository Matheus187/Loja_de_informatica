from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from ..database import engine
from pydantic import BaseModel 

router = APIRouter()

class ClienteSchema(BaseModel):
    nome: str
    telefone: str

@router.post("/")
def criar_cliente(cliente: ClienteSchema):
    with engine.begin() as conn:
        query = text("""
            INSERT INTO clientes (nome, telefone)
            VALUES (:nome, :telefone)
            RETURNING id
        """)
        result = conn.execute(query, {"nome": cliente.nome, "telefone": cliente.telefone})
        return {"id": result.scalar(), "message": "Cliente cadastrado com sucesso"}

@router.get("/")
def listar_clientes():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM clientes")).mappings().fetchall()
        return [dict(row) for row in result]

@router.get("/{id}")
def obter_cliente(id: int):
    with engine.connect() as conn:
        query = text("SELECT * FROM clientes WHERE id = :id")
        result = conn.execute(query, {"id": id}).mappings().fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return dict(result)

@router.put("/{id}")
def editar_cliente(id: int, cliente: ClienteSchema):
    with engine.begin() as conn:
        query = text("UPDATE clientes SET nome = :nome, telefone = :telefone WHERE id = :id")
        result = conn.execute(query, {"id": id, "nome": cliente.nome, "telefone": cliente.telefone})
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return {"message": "Dados do cliente atualizados"}

@router.delete("/{id}")
def deletar_cliente(id: int):
    with engine.begin() as conn:
        tem_vendas = conn.execute(
            text("SELECT 1 FROM vendas WHERE cliente_id = :id LIMIT 1"), {"id": id}
        ).fetchone()
        
        if tem_vendas:
            raise HTTPException(
                status_code=400, 
                detail="Não é possível excluir um cliente que já possui histórico de compras."
            )

        result = conn.execute(text("DELETE FROM clientes WHERE id = :id"), {"id": id})
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        return {"message": "Cliente removido com sucesso"}