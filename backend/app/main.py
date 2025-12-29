from fastapi import FastAPI
from backend.app.routes import vendas 

app = FastAPI()

app.include_router(vendas.router, prefix="/vendas", tags=["Vendas"])

@app.get("/")
def root():
    return {"message": "API de Vendas está rodando!"}