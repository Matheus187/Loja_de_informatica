from sqlalchemy import text
from backend.app.database import engine

def criar_tabelas():
    with engine.connect() as conn:
        print("Iniciando criação das tabelas...")

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS categorias(
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL UNIQUE
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS fornecedores(
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            telefone VARCHAR(20)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS clientes(
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            telefone VARCHAR(20)
        );
        """))
        
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS vendedores(
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            telefone VARCHAR(20),
            salario DECIMAL(10, 2),
            email VARCHAR(100) UNIQUE, 
            senha VARCHAR(100)         
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS produtos(
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT,
            preco DECIMAL(10, 2) NOT NULL,
            estoque INTEGER DEFAULT 0,
            categoria_id INTEGER REFERENCES categorias(id)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS vendas(
            id SERIAL PRIMARY KEY,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metodo_pagamento VARCHAR(50),
            cliente_id INTEGER REFERENCES clientes(id),
            vendedor_id INTEGER REFERENCES vendedores(id)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS itens_venda(
            venda_id INTEGER REFERENCES vendas(id),
            produto_id INTEGER REFERENCES produtos(id),
            quantidade INTEGER NOT NULL,
            preco_unitario DECIMAL(10, 2) NOT NULL,
            PRIMARY KEY (venda_id, produto_id)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS fornecedores_produtos (
            fornecedor_id INTEGER REFERENCES fornecedores(id),
            produto_id INTEGER REFERENCES produtos(id),
            PRIMARY KEY (fornecedor_id, produto_id)
        );
        """))

        conn.commit()
        print("Tabelas criadas com sucesso baseadas no diagrama!")

if __name__ == "__main__":
    criar_tabelas()