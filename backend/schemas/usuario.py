from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    """Schema base para usuário"""
    nome_usuario: str
    email: EmailStr

class UsuarioCriar(UsuarioBase):
    """Schema para criação de usuário"""
    senha: str

class UsuarioAtualizar(BaseModel):
    """Schema para atualização de usuário"""
    nome_usuario: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None

class UsuarioResposta(UsuarioBase):
    """Schema para resposta de usuário"""
    id: int
    ativo: bool
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    """Schema para login de usuário"""
    nome_usuario: str
    senha: str

class Token(BaseModel):
    """Schema para token de acesso"""
    access_token: str
    token_type: str

class TokenDados(BaseModel):
    """Schema para dados do token"""
    nome_usuario: Optional[str] = None
