from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import vendas, produtos, cliente, categorias

app = FastAPI()

# Permitir requisições do frontend (durante desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vendas.router, prefix="/vendas", tags=["Vendas"])
app.include_router(produtos.router, prefix="/produtos", tags=["Produtos"])
app.include_router(cliente.router, prefix="/clientes", tags=["Clientes"])
app.include_router(categorias.router, prefix="/categorias", tags=["Categorias"])


@app.get("/")
def root():
    return {"message": "API de Vendas está rodando!"}