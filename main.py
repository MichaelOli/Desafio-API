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
    redoc_url="/redoc"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["Rotas deAutenticação"])
app.include_router(documentos.router, prefix="/documentos", tags=["Rotas para realizar o CRUD do documentos"])

@app.get("/")
async def raiz():
    return {
        "mensagem": "API de Extração de Texto de PDF",
        "versao": "Desafio Central IT",
        "documentacao": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "mensagem": "API funcionando normalmente"}
