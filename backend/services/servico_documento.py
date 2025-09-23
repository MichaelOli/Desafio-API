import PyPDF2
import io
from fastapi import HTTPException, status, UploadFile
from typing import Tuple


class ServicoDocumento:
    """Classe para operações relacionadas a documentos PDF"""

    @staticmethod
    def validar_arquivo_pdf(arquivo: UploadFile) -> bool:
        """
        Valida se o arquivo é um PDF válido

        Args:
            arquivo: Arquivo enviado pelo usuário

        Returns:
            bool: True se o arquivo tiver a extensão PDF, False caso contrário
        """
        if not arquivo.filename:
            return False

        return arquivo.filename.lower().endswith(".pdf")

    @staticmethod
    def extrair_texto_pdf(conteudo_pdf: bytes) -> str:
        """
        Extrai texto de um arquivo PDF - PDF simples, sem imagens ou formatações complexas, vai ler PDF
        com texto apenas, estou usando o PyPDF2 para ler o PDF e extrair o texto e ele nao
        vai conseguir ler documentos com textos complexos e se ler vai bagunçar tudo.

        Args:
            conteudo_pdf: Conteúdo binário do PDF

        Returns:
            str: Texto extraído do PDF

        Raises:
            HTTPException: Se houver erro na extração
        """
        try:
            leitor_pdf = PyPDF2.PdfReader(io.BytesIO(conteudo_pdf))
            texto_extraido = ""

            for pagina in leitor_pdf.pages:
                texto_extraido += pagina.extract_text() + "\n"

            return texto_extraido.strip()

        except Exception as erro:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao extrair texto do PDF: {str(erro)}",
            )

    @staticmethod
    def processar_upload_pdf(arquivo: UploadFile) -> Tuple[str, int]:
        """
        Processa upload de PDF e extrai informações

        Args:
            arquivo: Arquivo PDF enviado

        Returns:
            Tuple[str, int]: (texto_extraido, tamanho_arquivo)

        Raises:
            HTTPException: Se arquivo for inválido ou erro na extração
        """
        # Validar se é PDF
        if not ServicoDocumento.validar_arquivo_pdf(arquivo):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Apenas arquivos PDF são aceitos",
            )

        # Ler conteúdo do arquivo
        conteudo_arquivo = arquivo.file.read()
        tamanho_arquivo = len(conteudo_arquivo)

        # Extrair texto
        texto_extraido = ServicoDocumento.extrair_texto_pdf(conteudo_arquivo)

        if not texto_extraido:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Não foi possível extrair texto do PDF",
            )

        return texto_extraido, tamanho_arquivo
