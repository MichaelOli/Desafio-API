from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentoBase(BaseModel):
    """Schema base para documento"""
    nome_arquivo: str
    texto_extraido: str

class DocumentoCriar(DocumentoBase):
    """Schema para criação de documento"""
    tamanho_arquivo: int

class DocumentoAtualizar(BaseModel):
    """Schema para atualização de documento"""
    nome_arquivo: Optional[str] = None
    texto_extraido: Optional[str] = None

class DocumentoResposta(DocumentoBase):
    """Schema para resposta de documento"""
    id: int
    tamanho_arquivo: int
    usuario_id: int
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None

    class Config:
        from_attributes = True

class DocumentoLista(BaseModel):
    """Schema para listagem de documentos"""
    id: int
    nome_arquivo: str
    tamanho_arquivo: int
    data_criacao: datetime

    class Config:
        from_attributes = True
