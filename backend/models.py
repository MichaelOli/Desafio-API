from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import base

class DocumentoTexto(base):
    __tablename__ = "documentos_texto"
    
    id = Column(Integer, primary_key=True, index=True)
    nome_arquivo = Column(String(255), nullable=False)
    texto_extraido = Column(Text, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())