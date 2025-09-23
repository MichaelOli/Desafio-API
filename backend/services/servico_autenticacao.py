import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.database import conexao_db
from backend.models import Usuario
from backend.schemas.usuario import TokenDados

# Configurações de segurança
CHAVE_SECRETA = os.getenv("CHAVE_SECRETA")
ALGORITMO_JWT = "HS256"
MINUTOS_EXPIRACAO_TOKEN = 30

# Contexto para criptografia de senhas
contexto_senhas = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de autenticação Bearer Token
esquema_autenticacao = HTTPBearer()


class ServicoAutenticacao:
    """Service para operações de autenticação e autorização"""

    @staticmethod
    def verificar_senha(senha_digitada: str, hash_senha: str) -> bool:
        """
        Verifica se a senha está correta

        Args:
            senha_digitada: Senha digitada pelo usuário
            hash_senha: Hash da senha armazenado no banco

        Returns:
            bool: True se senha correta, False caso contrário
        """
        return contexto_senhas.verify(senha_digitada, hash_senha)

    @staticmethod
    def gerar_hash_senha(senha: str) -> str:
        """
        Gera hash da senha

        Args:
            senha: Senha digitada pelo usuário

        Returns:
            str: Hash criptogradado da senha
        """
        return contexto_senhas.hash(senha)

    @staticmethod
    def criar_token_acesso(
        dados: dict, tempo_expiracao: Optional[timedelta] = None
    ) -> str:
        """
        Cria token de acesso JWT

        Args:
            dados: Dados para incluir no token
            tempo_expiracao: Tempo de expiração personalizado

        Returns:
            str: Token JWT
        """
        dados_para_codificar = dados.copy()
        if tempo_expiracao:
            data_expiracao = datetime.utcnow() + tempo_expiracao
        else:
            data_expiracao = datetime.utcnow() + timedelta(
                minutes=MINUTOS_EXPIRACAO_TOKEN
            )

        dados_para_codificar.update({"exp": data_expiracao})
        token_jwt = jwt.encode(dados_para_codificar, CHAVE_SECRETA, algorithm=ALGORITMO_JWT)
        return token_jwt

    @staticmethod
    def verificar_token(token: str, excecao_credenciais) -> TokenDados:
        """
        Verifica e decodifica o token JWT

        Args:
            token: Token JWT
            excecao_credenciais: Exceção para lançar em caso de erro

        Returns:
            TokenDados: Dados do token decodificado

        Raises:
            HTTPException: Se token inválido
        """
        try:
            dados_token = jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO_JWT])
            nome_usuario: str = dados_token.get("sub")
            if nome_usuario is None:
                raise excecao_credenciais
            dados_validados = TokenDados(nome_usuario=nome_usuario)
        except JWTError:
            raise excecao_credenciais
        return dados_validados

    @staticmethod
    def obter_usuario_atual(
        credenciais: HTTPAuthorizationCredentials = Depends(esquema_autenticacao),
        db: Session = Depends(conexao_db),
    ) -> Usuario:
        """
        Obtém o usuário atual baseado no token

        Args:
            credenciais: Credenciais de autorização
            db: Sessão do banco de dados

        Returns:
            Usuario: Usuário atual

        Raises:
            HTTPException: Se token inválido ou usuário não encontrado
        """
        excecao_credenciais = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais ou o usuário não existe no sistema",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token = credenciais.credentials
        dados_token = ServicoAutenticacao.verificar_token(token, excecao_credenciais)

        usuario = (
            db.query(Usuario)
            .filter(Usuario.nome_usuario == dados_token.nome_usuario)
            .first()
        )

        if usuario is None:
            raise excecao_credenciais

        return usuario

    @staticmethod
    def gerar_token_para_usuario(nome_usuario: str) -> str:
        """
        Gera token de acesso para um usuário

        Args:
            nome_usuario: Nome de usuário

        Returns:
            str: Token JWT
        """
        tempo_expiracao_token = timedelta(minutes=MINUTOS_EXPIRACAO_TOKEN)
        return ServicoAutenticacao.criar_token_acesso(
            {"sub": nome_usuario}, tempo_expiracao_token
        )
