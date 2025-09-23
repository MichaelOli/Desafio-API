# Documentação da API - Extração de Texto de PDF - Rotas

## Base URL

```
http://localhost:8000
```

## Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação. Para acessar endpoints protegidos, inclua o token no header Authorization:

```
Authorization: Bearer SEU_TOKEN
```

## Endpoints de Autenticação

### POST /auth/registrar

Registra um novo usuário no sistema.

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
  "email": "usuario@exemplo.com",
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

Retorna os dados do usuário autenticado.

**Headers:**

```
Authorization: Bearer SEU_TOKEN
```

**Response (200 OK):**

```json
{
  "id": 1,
  "nome_usuario": "usuario_teste",
  "email": "usuario@exemplo.com",
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
  "texto_extraido": "Conteúdo extraído do PDF...",
  "tamanho_arquivo": 1024000,
  "usuario_id": 1,
  "data_criacao": "2025-09-23T00:59:14",
  "data_atualizacao": null
}
```

**Códigos de Erro:**

- `400 Bad Request`: Arquivo inválido ou erro na extração
- `401 Unauthorized`: Token inválido ou expirado
- `422 Unprocessable Entity`: Erro de validação

### GET /documentos/

Lista todos os documentos do usuário autenticado.

**Headers:**

```
Authorization: Bearer SEU_TOKEN_AQUI
```

**Query Parameters:**

- `pular` (int, opcional): Número de registros para pular (padrão: 0)
- `limite` (int, opcional): Número máximo de registros (padrão: 100)

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

- `401 Unauthorized`: Token inválido ou expirado

### GET /documentos/{id}

Obtém um documento específico pelo ID.

**Headers:**

```
Authorization: Bearer SEU_TOKEN_AQUI
```

**Path Parameters:**

- `id` (int): ID do documento

**Response (200 OK):**

```json
{
  "id": 1,
  "nome_arquivo": "documento.pdf",
  "texto_extraido": "Conteúdo extraído do PDF...",
  "tamanho_arquivo": 1024000,
  "usuario_id": 1,
  "data_criacao": "2025-09-23T00:59:14",
  "data_atualizacao": null
}
```

**Códigos de Erro:**

- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Documento não encontrado

### PUT /documentos/{id}

Atualiza um documento existente.

**Headers:**

```
Authorization: Bearer SEU_TOKEN_AQUI
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

- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Documento não encontrado
- `422 Unprocessable Entity`: Erro de validação

### DELETE /documentos/{id}

Deleta um documento.

**Headers:**

```
Authorization: Bearer SEU_TOKEN_AQUI
```

**Path Parameters:**

- `id` (int): ID do documento

**Response (204 No Content):**

```
(Sem conteúdo)
```

**Códigos de Erro:**

- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Documento não encontrado

## Códigos de Status HTTP

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `204 No Content`: Operação bem-sucedida sem retorno
- `400 Bad Request`: Dados inválidos na requisição
- `401 Unauthorized`: Token inválido ou expirado
- `404 Not Found`: Recurso não encontrado
- `422 Unprocessable Entity`: Erro de validação de dados

## Limitações e Validações

### Upload de Arquivos

- **Tipo permitido**: Apenas arquivos PDF
- **Validação**: Verificação de extensão e tipo MIME
- **Tamanho**: Limitado pela configuração do servidor

### Autenticação

- **Expiração do token**: 30 minutos
- **Algoritmo**: HS256
- **Formato**: Bearer token

### Dados de Usuário

- **Nome de usuário**: Único, obrigatório
- **Email**: Único, formato válido obrigatório
- **Senha**: Mínimo de caracteres (configurável)

## Exemplos de Uso Completos

### Fluxo Completo: Registro, Login e Upload

1. **Registrar usuário:**

```bash
curl -X POST "http://localhost:8000/auth/registrar" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_usuario": "usuario_teste",
    "email": "usuario@exemplo.com",
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
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -F "arquivo=@documento.pdf"
```

4. **Listar documentos:**

```bash
curl -X GET "http://localhost:8000/documentos/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## Troubleshooting

### Erro 401 Unauthorized

- Verifique se o token está correto
- Confirme se o token não expirou (30 minutos)
- Certifique-se de incluir "Bearer " antes do token

### Erro 400 Bad Request no Upload

- Verifique se o arquivo é um PDF válido
- Confirme se o arquivo não está corrompido
- Verifique se o arquivo tem conteúdo de texto

### Erro 422 Unprocessable Entity

- Verifique o formato dos dados enviados
- Confirme se todos os campos obrigatórios estão preenchidos
- Verifique se os tipos de dados estão corretos

## Rate Limiting

Atualmente não há rate limiting implementado, mas é recomendado para produção.

## Versionamento

A API está na versão 1.0.0. Mudanças significativas serão versionadas adequadamente.
