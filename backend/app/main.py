from fastapi import FastAPI
from backend.app.routers import (
    vendas, 
    produtos, 
    cliente, 
    categorias, 
    dashboard, 
    relatorio
)
app = FastAPI()
app.include_router(vendas.router, prefix="/vendas", tags=["Vendas"])
app.include_router(produtos.router, prefix="/produtos", tags=["Produtos"])
app.include_router(cliente.router, prefix="/clientes", tags=["Clientes"])
app.include_router(categorias.router, prefix="/categorias", tags=["Categorias"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(relatorio.router, prefix="/relatorios", tags=["Relatórios Específicos"])

@app.get("/")
def root():
    return {"message": "API de Vendas está rodando!"}