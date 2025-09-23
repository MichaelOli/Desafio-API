from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

URL_DATABASE = os.getenv("DATABASE_URL", "sqlite:///./desafio_api.db")

engine = create_engine(URL_DATABASE)
sessaolocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

def conexao_db():
    db = sessaolocal()
    try:
        yield db
    finally:
        db.close()
