from fastapi import FastAPI
from backend.app.routers import vendas, produtos, cliente, categorias

app = FastAPI()
app.include_router(vendas.router, prefix="/vendas", tags=["Vendas"])
app.include_router(produtos.router, prefix="/produtos", tags=["Produtos"])
app.include_router(cliente.router, prefix="/clientes", tags=["Clientes"])
app.include_router(categorias.router, prefix="/categorias", tags=["Categorias"])

@app.get("/")
def root():
    return {"message": "API de Vendas está rodando!"}