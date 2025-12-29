import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Carrega as variáveis do arquivo .env
load_dotenv()

# 2. Pega a URL de conexão lá de dentro
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Verifica se achou a URL (pra não dar erro silencioso)
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não foi encontrada no arquivo .env")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()