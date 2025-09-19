from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.database import conexao_db
from backend.models import Usuario
from backend.schemas.usuario import UsuarioCriar, UsuarioResposta, UsuarioLogin, Token
from backend.services.servico_usuario import ServicoUsuario
from backend.services.servico_autenticacao import ServicoAutenticacao

router = APIRouter()

@router.post("/registrar", response_model=UsuarioResposta, status_code=status.HTTP_201_CREATED)
async def registrar_usuario(usuario: UsuarioCriar, db: Session = Depends(conexao_db)):
    """
    Registra um novo usuário no sistema
    
    - **nome_usuario**: Nome de usuário único
    - **email**: Email único do usuário
    - **senha**: Senha do usuário (será criptografada)
    """
    return ServicoUsuario.criar_usuario(db, usuario)

@router.post("/login", response_model=Token)
async def login_usuario(credenciais: UsuarioLogin, db: Session = Depends(conexao_db)):
    """
    Realiza login do usuário e retorna token de acesso
    
    - **nome_usuario**: Nome de usuário
    - **senha**: Senha do usuário
    """
    # Validar credenciais
    usuario = ServicoUsuario.validar_credenciais(db, credenciais.nome_usuario, credenciais.senha)
    
    # Gerar token
    token_acesso = ServicoAutenticacao.gerar_token_para_usuario(usuario.nome_usuario)
    
    return {"access_token": token_acesso, "token_type": "bearer"}

@router.get("/me", response_model=UsuarioResposta)
async def obter_dados_usuario_atual(usuario_atual: Usuario = Depends(ServicoAutenticacao.obter_usuario_atual)):
    """
    Retorna os dados do usuário logado
    
    Precisa de autenticação via token JWT
    """
    return usuario_atual
