from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    estoque: int
    categoria_id: int

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int
    
    class Config:
        from_attributes = True 

class ItemVendaSchema(BaseModel):
    produto_id: int
    quantidade: int
    
class VendaCreate(BaseModel):
    cliente_id: int
    vendedor_id: int
    metodo_pagamento: str
    itens: List[ItemVendaSchema] 

class VendaResponse(BaseModel):
    id: int
    data: datetime
    total: float 