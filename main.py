from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, base
from backend.routers import auth, documentos

# Criar tabelas no banco de dados
base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Extração de Texto de PDF",
    description="API para upload de arquivos PDF, desafio Central IT, para extração de texto e gerenciamento de documentos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo as rotas
app.include_router(auth.router, prefix="/auth", tags=["Rotas deAutenticação"])
app.include_router(
    documentos.router,
    prefix="/documentos",
    tags=["Rotas para realizar o CRUD do documentos"]
)


@app.get("/funcionando", tags=["Verifica se a API esta funcionando"])
async def testa_se_api_esta_funcionando():
    return {
        "mensagem": "API de Extração de Texto de PDF",
        "versao": "Desafio Central IT",
        "documentacao": "/docs",
    }
