# Documentação da API - Extração de Texto de PDF - Rotas

## Base URL

```
http://localhost:8000
```

## autenticacao

A API utiliza JWT (JSON Web Tokens) para autenticacao. Para acessar endpoints protegidos, inclua o token no header Authorization:

```
Authorization: Bearer SEU_TOKEN
```
Ou utilize o Swagger para navegar entre os endpoints.
## Endpoints de autenticacao

### POST /auth/registrar

Registra um novo usuario no sistema.

**Request Body:**

```json
{
  "nome_usuario": "string",
  "email": "string",
  "senha": "string"
}
```

**Response (201 Created):**

```json
{
  "id": 1,
  "nome_usuario": "usuario_teste",
  "email": "usuario@teste.com",
  "ativo": true,
  "data_criacao": "2025-09-23T00:56:04",
  "data_atualizacao": null
}
```

**Códigos de Erro:**

- `400 Bad Request`: Dados invalidos ou usuario ja existe
- `422 Unprocessable Entity`: Erro de validacao

### POST /auth/login

Autentica um usuario e retorna token de acesso.

**Request Body:**

```json
{
  "nome_usuario": "string",
  "senha": "string"
}
```

**Response (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Códigos de Erro:**

- `401 Unauthorized`: Credenciais invalidas
- `422 Unprocessable Entity`: Erro de validacao

### GET /auth/eu

Retorna os dados do usuario autenticado.

**Headers:**

```
Authorization: Bearer SEU_TOKEN
```

**Response (200 OK):**

```json
{
  "id": 1,
  "nome_usuario": "usuario_teste",
  "email": "usuario@teste.com",
  "ativo": true,
  "data_criacao": "2025-09-23T00:56:04",
  "data_atualizacao": null
}
```

**Códigos de Erro:**

- `401 Unauthorized`: Token invalido ou expirado

## Endpoints de Documentos

### POST /documentos/upload

Upload de arquivo PDF e extração de texto. Necessita esta autenticado.

**Headers:**

```
Authorization: Bearer SEU_TOKEN
Content-Type: multipart/form-data
```

**Request Body:**

```
arquivo: [arquivo PDF]
```

**Response (201 Created):**

```json
{
  "id": 1,
  "nome_arquivo": "documento.pdf",
  "texto_extraido": "conteudo extraido do PDF...",
  "tamanho_arquivo": 1024000,
  "usuario_id": 1,
  "data_criacao": "2025-09-23T00:59:14",
  "data_atualizacao": null
}
```

**Codigos de Erro:**

- `400 Bad Request`: Arquivo invalido ou erro na extracao
- `401 Unauthorized`: Token invalido ou expirado
- `422 Unprocessable Entity`: Erro de validacao

### GET /documentos/

Lista todos os documentos do usuario autenticado.

**Headers:**

```
Authorization: Bearer SEU_TOKEN
```

**Query Parameters:**

-Levando em consideracao que a api possa ter muitos documentos.

- `pular` (int, opcional): Numero de registros para pular (padrao: 0)
- `limite` (int, opcional): Numero maximo de registros (padrao: 100)

**Response (200 OK):**

```json
[
  {
    "id": 1,
    "nome_arquivo": "documento.pdf",
    "tamanho_arquivo": 1024000,
    "data_criacao": "2025-09-23T00:59:14"
  }
]
```

**Códigos de Erro:**

- `401 Unauthorized`: Token invalido ou expirado

### GET /documentos/{id}

obtem um documento especifico pelo ID.

**Headers:**

```
Authorization: Bearer SEU_TOKEN
```

**Path Parameters:**

- `id` (int): ID do documento

**Response (200 OK):**

```json
{
  "id": 1,
  "nome_arquivo": "documento.pdf",
  "texto_extraido": "conteudo extraido do PDF...",
  "tamanho_arquivo": 1024000,
  "usuario_id": 1,
  "data_criacao": "2025-09-23T00:59:14",
  "data_atualizacao": null
}
```

**Códigos de Erro:**

- `401 Unauthorized`: Token invalido ou expirado
- `404 Not Found`: Documento nao encontrado

### PUT /documentos/{id}

Atualiza um documento existente.

**Headers:**

```
Authorization: Bearer SEU_TOKEN
Content-Type: application/json
```

**Path Parameters:**

- `id` (int): ID do documento

**Request Body:**

```json
{
  "nome_arquivo": "novo_nome.pdf",
  "texto_extraido": "Texto atualizado..."
}
```

**Response (200 OK):**

```json
{
  "id": 1,
  "nome_arquivo": "novo_nome.pdf",
  "texto_extraido": "Texto atualizado...",
  "tamanho_arquivo": 1024000,
  "usuario_id": 1,
  "data_criacao": "2025-09-23T00:59:14",
  "data_atualizacao": "2025-09-23T01:30:00"
}
```

**Códigos de Erro:**

- `401 Unauthorized`: Token invalido ou expirado
- `404 Not Found`: Documento nao encontrado
- `422 Unprocessable Entity`: Erro de validacao

### DELETE /documentos/{id}

Deleta um documento.

**Headers:**

```
Authorization: Bearer SEU_TOKEN
```

**Path Parameters:**

- `id` (int): ID do documento

**Response (204 No Content):**

```
(Sem conteudo)
```

**Códigos de Erro:**

- `401 Unauthorized`: Token invalido ou expirado
- `404 Not Found`: Documento nao encontrado

## Códigos de Status HTTP

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `204 No Content`: Operação bem-sucedida sem retorno
- `400 Bad Request`: Dados invalidos na requisição
- `401 Unauthorized`: Token invalido ou expirado
- `404 Not Found`: Recurso nao encontrado
- `422 Unprocessable Entity`: Erro de validacao de dados

## Limitações e Validações

### Upload de Arquivos

- **Tipo permitido**: Apenas arquivos PDF
- **validacao**: verificacao de extensao
- **Tamanho**: Limitado pela configuracao do servidor/database plugado na api

### autenticacao

- **Expiração do token**: 30 minutos
- **Algoritmo**: HS256
- **Formato**: Bearer token

### Dados de usuario

- **Nome de usuario**: unico, obrigatorio
- **Email**: unico, formato valido obrigatorio
- **Senha**: Mínimo de caracteres (configurável)

## testes de Uso Completos

### Fluxo Completo: Registro, Login e Upload

1. **Registrar usuario:**

```bash
curl -X POST "http://localhost:8000/auth/registrar" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_usuario": "usuario_teste",
    "email": "usuario@teste.com",
    "senha": "senha123"
  }'
```

2. **Fazer login:**

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_usuario": "usuario_teste",
    "senha": "senha123"
  }'
```

3. **Upload de PDF:**

```bash
curl -X POST "http://localhost:8000/documentos/upload" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -F "arquivodocumento.pdf"
```

4. **Listar documentos:**

```bash
curl -X GET "http://localhost:8000/documentos/" \
  -H "Authorization: Bearer SEU_TOKEN"
```

## Troubleshooting

### Erro 401 Unauthorized

- Verifique se o token tá correto
- Confirme se o token nao expirou (30 minutos)
- Certifique-se de incluir "Bearer " antes do token caso utilize requisicções com curl ou invoke

### Erro 400 Bad Request no Upload

- Verifique se o arquivo é um PDF valido
- Confirme se o arquivo nao está corrompido
- Verifique se o arquivo tem conteudo de texto

### Erro 422 Unprocessable Entity

- Verifique o formato dos dados enviados
- Confirme se todos os campos obrigatorios estão preenchidos
- Verifique se os tipos de dados estão corretos

