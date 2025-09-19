from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.models import Usuario
from backend.schemas.usuario import UsuarioCriar, UsuarioAtualizar
from backend.utils.autenticacao import gerar_hash_senha, verificar_senha

class ServicoUsuario:
    """Service para operações relacionadas a usuarios"""
    
    @staticmethod
    def verificar_usuario_existente(db: Session, nome_usuario: str, email: str) -> Usuario:
        """
        Verifica se já existe usuario com nome ou email
        
        Args:
            db: Sessão do banco de dados
            nome_usuario: Nome de usuario para verificar
            email: Email para verificar
            
        Returns:
            Usuario: usuario existente ou None
        """
        return db.query(Usuario).filter(
            (Usuario.nome_usuario == nome_usuario) | 
            (Usuario.email == email)
        ).first()
    
    @staticmethod
    def criar_usuario(db: Session, usuario_dados: UsuarioCriar) -> Usuario:
        """
        Cria um novo usuario no sistema
        
        Args:
            db: Sessão do banco de dados
            usuario_dados: Dados do usuario para criação
            
        Returns:
            Usuario: usuario criado
            
        Raises:
            HTTPException: Se usuario já existir
        """
        # Verificar se usuario já existe
        usuario_existente = ServicoUsuario.verificar_usuario_existente(
            db, usuario_dados.nome_usuario, usuario_dados.email
        )
        
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nome de usuario ou email já cadastrado"
            )
        
        # Criar novo usuario
        senha_hash = gerar_hash_senha(usuario_dados.senha)
        db_usuario = Usuario(
            nome_usuario=usuario_dados.nome_usuario,
            email=usuario_dados.email,
            senha_hash=senha_hash
        )
        
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        
        return db_usuario
    
    @staticmethod
    def buscar_usuario_por_nome(db: Session, nome_usuario: str) -> Usuario:
        """
        Busca usuario pelo nome de usuario
        
        Args:
            db: Sessão do banco de dados
            nome_usuario: Nome de usuario para buscar
            
        Returns:
            Usuario: Usuario encontrado ou None
        """
        return db.query(Usuario).filter(
            Usuario.nome_usuario == nome_usuario
        ).first()
    
    @staticmethod
    def validar_credenciais(db: Session, nome_usuario: str, senha: str) -> Usuario:
        """
        Valida credenciais de login
        
        Args:
            db: Sessão do banco de dados
            nome_usuario: Nome de usuario
            senha: Senha do usuario
            
        Returns:
            Usuario: usuario válido
            
        Raises:
            HTTPException: Se credenciais inválidas ou usuario inativo
        """
        # Buscar usuario
        usuario = ServicoUsuario.buscar_usuario_por_nome(db, nome_usuario)
        
        if not usuario or not verificar_senha(senha, usuario.senha_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas ou usuario nao existe no sistema",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not usuario.ativo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="usuario inativo"
            )
        
        return usuario
    
    @staticmethod
    def atualizar_usuario(db: Session, usuario_id: int, dados_atualizacao: UsuarioAtualizar) -> Usuario:
        """
        Atualiza dados de um usuario
        
        Args:
            db: Sessão do banco de dados
            usuario_id: ID do usuario
            dados_atualizacao: Dados para atualização
            
        Returns:
            Usuario: usuario atualizado
            
        Raises:
            HTTPException: Se usuario não encontrado
        """
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="usuario não encontrado"
            )
        
        # Atualizar apenas campos fornecidos
        dados_dict = dados_atualizacao.dict(exclude_unset=True)
        
        # Se senha for fornecida, gerar hash
        if 'senha' in dados_dict:
            dados_dict['senha_hash'] = gerar_hash_senha(dados_dict.pop('senha'))
        
        for campo, valor in dados_dict.items():
            setattr(usuario, campo, valor)
        
        db.commit()
        db.refresh(usuario)
        
        return usuario
