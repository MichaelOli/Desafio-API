from backend.schemas.documento import (
    DocumentoResposta,
    DocumentoLista,
    DocumentoAtualizar,
)
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from backend.services.servico_autenticacao import ServicoAutenticacao
from backend.services.servico_documento import ServicoDocumento
from backend.models import DocumentoTexto, Usuario
from backend.database import conexao_db
from sqlalchemy.orm import Session
from typing import List


router = APIRouter()


@router.post(
    "/upload", response_model=DocumentoResposta, status_code=status.HTTP_201_CREATED
)
async def upload_documento(
    arquivo: UploadFile = File(...),
    db: Session = Depends(conexao_db),
    usuario_atual: Usuario = Depends(ServicoAutenticacao.obter_usuario_atual),
):
    """
    Estou usando o PyPDF2 para ler o PDF e extrair o texto e ele nao
    vai conseguir ler documentos com textos de formatacao
    e/ou imagens complexos e se ler pode acabar desestruturando os dados.

    - **Observacao**: Antes de fazer o upload, é preciso realizar autenticacao nas rotas acima
    do contrario, retorna 403 Not authenticated
    - **arquivo**: Arquivo PDF para upload
    - **Retorna**: Dados do documento criado com texto extraído
    """
    # Processar PDF usando service
    texto_extraido, tamanho_arquivo = ServicoDocumento.processar_upload_pdf(arquivo)

    # Criar documento no banco
    documento = DocumentoTexto(
        nome_arquivo=arquivo.filename,
        texto_extraido=texto_extraido,
        tamanho_arquivo=tamanho_arquivo,
        usuario_id=usuario_atual.id,
    )

    db.add(documento)
    db.commit()
    db.refresh(documento)

    return documento


@router.get("/", response_model=List[DocumentoLista])
async def listar_documentos(
    pular: int = 0,
    limite: int = 100,
    db: Session = Depends(conexao_db),
    usuario_atual: Usuario = Depends(ServicoAutenticacao.obter_usuario_atual),
):
    """
    Lista os documentos que o usuário logado subiu.

    - **pular**: Número de registros para pular (paginação)
    - **limite**: Número máximo de registros por página
    """
    documentos = (
        db.query(DocumentoTexto)
        .filter(DocumentoTexto.usuario_id == usuario_atual.id)
        .offset(pular)
        .limit(limite)
        .all()
    )

    return documentos


@router.get("/{id_documento}", response_model=DocumentoResposta)
async def obter_documento(
    id_documento: int,
    db: Session = Depends(conexao_db),
    usuario_atual: Usuario = Depends(ServicoAutenticacao.obter_usuario_atual),
):
    """
    Consulta um documento específico pelo ID

    - **id_documento**: ID do documento
    """
    documento = (
        db.query(DocumentoTexto)
        .filter(
            DocumentoTexto.id == id_documento,
            DocumentoTexto.usuario_id == usuario_atual.id,
        )
        .first()
    )

    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Documento nao encontrado"
        )

    return documento


@router.put("/{id_documento}", response_model=DocumentoResposta)
async def atualizar_documento(
    id_documento: int,
    documento_atualizacao: DocumentoAtualizar,
    db: Session = Depends(conexao_db),
    usuario_atual: Usuario = Depends(ServicoAutenticacao.obter_usuario_atual),
):
    """
    Atualiza um documento existente

    - **id_documento**: ID do documento
    - **documento_atualizacao**: Dados para atualizacao
    """
    documento = (
        db.query(DocumentoTexto)
        .filter(
            DocumentoTexto.id == id_documento,
            DocumentoTexto.usuario_id == usuario_atual.id,
        )
        .first()
    )

    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Documento nao encontrado"
        )

    # Atualizar apenas campos fornecidos
    dados_atualizacao = documento_atualizacao.dict(exclude_unset=True)
    for campo, valor in dados_atualizacao.items():
        setattr(documento, campo, valor)

    db.commit()
    db.refresh(documento)

    return documento


@router.delete("/{id_documento}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_documento(
    id_documento: int,
    db: Session = Depends(conexao_db),
    usuario_atual: Usuario = Depends(ServicoAutenticacao.obter_usuario_atual),
):
    """
    Deleta um documento

    - **id_documento**: ID do documento
    """
    documento = (
        db.query(DocumentoTexto)
        .filter(
            DocumentoTexto.id == id_documento,
            DocumentoTexto.usuario_id == usuario_atual.id,
        )
        .first()
    )

    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Documento nao encontrado"
        )

    db.delete(documento)
    db.commit()

    return None
