# API de Extração de Texto de PDF

## Descrição

API desenvolvida em FastAPI para upload de arquivos PDF, extraçao automatica de texto e gerenciamento de documentos. O sistema implementa autenticaçao JWT, CRUD completo e documentação automática via Swagger.

## Funcionalidades

- **Upload de PDF**: Recebimento e validaçao de arquivos PDF
- **Extração de Texto**: Extração automática de texto usando PyPDF2
- **Autenticação JWT**: Sistema seguro de login e registro
- **CRUD Completo**: Criar, listar, consultar, atualizar e deletar documentos
- **Documentação Automática**: Swagger UI integrado
- **validaçao de Dados**: Pydantic para validaçao eficiente
- **Banco SQLite**: Persistência de dados local

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para Python
- **SQLite**: Banco de dados leve e eficiente
- **JWT**: Autenticação stateless
- **PyPDF2**: Extração de texto de PDFs
- **Pydantic**: validaçao e serialização de dados
- **Docker**: Containerização da aplicação
- **Poetry**: Gerenciamento de dependências

## Pré-requisitos

- Python 3.10 ou superior
- Poetry (gerenciador de dependências)
- Docker (opcional, para containerização)

## Instalação e Execuçao

### Método 1: Poetry (Recomendado)

1. Clone o repositório:

```bash
git clone <https://github.com/MichaelOli/Desafio-API/>
cd Desafio_API
```

2. Instale as dependências:

```bash
pip install poetry
```

```bash
poetry install
```

3. Execute a aplicação:

```bash
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Método 2: pip + requirements.txt

1. Clone o repositório:

```bash
git clone <https://github.com/MichaelOli/Desafio-API/>
cd Desafio_API
```

2. Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Método 3: Docker

1. Execute com Docker Compose:

```bash
docker-compose up -d
```

## Acesso à API

- **API Base**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Testar se a api ta funcionando**: http://localhost:8000/funcionando

## Estrutura do Projeto

```
Desafio_API/
├── backend/
│   ├── database.py          # Configuração do banco
│   ├── models.py            # Modelos SQLAlchemy
│   ├── routers/             # Rotas da API
│   │   ├── auth.py         # Autenticação
│   │   └── documentos.py   # CRUD de documentos
│   ├── schemas/             # Schemas Pydantic
│   │   ├── usuario.py      # Schemas de usuario
│   │   └── documento.py    # Schemas de documento
│   └── services/            # Lógica de negócio
│       ├── servico_autenticacao.py
│       ├── servico_documento.py
│       └── servico_usuario.py
├── main.py                  # Aplicação principal
├── pyproject.toml          # Dependências Poetry
├── docker-compose.yml      # Configuração Docker
├── Dockerfile             # Imagem Docker
└── README.md              # Este arquivo
```

## Endpoints da API

### Autenticação

- **POST /auth/registrar**: Registrar novo usuario
- **POST /auth/login**: Fazer login e obter token
- **GET /auth/me**: Obter dados do usuario atual

- **Observações:** No proprio Swagger ao obter o token, é possivel informar o token gerado no simbolo do cadeado para que possa utilizar as rotas que realizam as operações de CRUD.

### Documentos

- **POST /documentos/upload**: Upload de arquivo PDF
- **GET /documentos/**: Listar documentos do usuario
- **GET /documentos/{id}**: Obter documento específico
- **PUT /documentos/{id}**: Atualizar documento
- **DELETE /documentos/{id}**: Deletar documento

## Exemplos de Uso

### 1. Registrar usuario

```bash
curl -X POST "http://localhost:8000/auth/registrar" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_usuario": "usuario_teste",
    "email": "usuario@exemplo.com",
    "senha": "senha123"
  }'
```

### 2. Fazer Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_usuario": "usuario_teste",
    "senha": "senha123"
  }'
```

### 3. Upload de PDF

```bash
curl -X POST "http://localhost:8000/documentos/upload" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -F "arquivo=@documento.pdf"
```

### 4. Listar Documentos

```bash
curl -X GET "http://localhost:8000/documentos/" \
  -H "Authorization: Bearer SEU_TOKEN"
```

## Segurança

### Autenticação JWT

- Tokens com expiração de 30 minutos
- Algoritmo HS256 para assinatura
- Chave secreta configurável via variável de ambiente

### validaçao de Dados

- validaçao automática de tipos e formatos
- Sanitização de entradas do usuario
- validaçao de arquivos PDF

### Criptografia

- Senhas hasheadas com bcrypt
- Salt automático para cada senha
- Rounds de hash configuráveis

### CORS

- Configuração flexível para desenvolvimento
- Headers de segurança implementados
- Métodos HTTP restritos conforme necessário

## Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DATABASE_URL=sqlite:///./desafio_api.db
```

## Desenvolvimento

### Executar em Modo Desenvolvimento

```bash
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Executar Testes

```bash
poetry run pytest
```

### Formatação de Código

```bash
poetry run black .
poetry run isort .
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Autor

Desenvolvido por Michael Oliveira Ribeiro
Email: michaeloliveira38@gmail.com
