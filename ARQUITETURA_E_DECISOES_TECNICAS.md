# API de Extração de Texto de PDF - Arquitetura e Decisões Técnicas

## Visão Geral do Projeto

Esta API foi desenvolvida como resposta ao **Desafio Técnico - FastAPI + SQLite** da Central IT, com o objetivo de demonstrar competências em desenvolvimento de APIs RESTful, processamento e manipulacao de documentos em formanto PDF, como bônus implementação de autenticação com token JWT.

### Objetivos Alcançados

- Endpoint para upload de arquivos PDF
- Extração automática de texto de documentos PDF
- CRUD completo para gerenciamento de documentos
- Documentação interativa com Swagger
- Sistema de autenticação JWT
- Persistência de dados com SQLite

---

## Arquitetura da Aplicação

### Arquitetura escolhida para o projeto: **Service Layer Pattern**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ROUTERS       │    │    SERVICES     │    │    MODELS       │
│   (Controllers) │───▶│  (Lógica de     │───▶│  (Entidades do  │
│                 │    │   mercado)      │    │   banco)        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SCHEMAS       │    │   UTILITIES     │    │   DATABASE      │
│   (Validacao)   │    │   (Helpers)     │    │   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Por que escolhi esta arquitetura?**

1. **Separação de Responsabilidades**: Cada camada tem uma responsabilidade específica
2. **Testabilidade**: Serviços podem ser testados de forma independentemente
3. **Manutenibilidade**: Mudanças em uma camada não afetam as outras
4. **Reutilização**: Serviços podem ser reutilizados em diferentes routers
5. **Escalabilidade**: Possibilidade em adicionar novas funcionalidades 

---

## Stack Tecnológica e Justificativas

### **FastAPI** - Framework Web

### **Por que FastAPI?** - Além de ter sido solicitação do desafio:

- **Performance**: Uma das APIs mais rápidas do Python
- **Type Hints**: Validação automática de tipos
- **Documentação**: Swagger/OpenAPI integrado
- **Async/Await**: Suporte nativo para operações assíncronas
- **Validação de Dados**: Integração com Pydantic

### **SQLite** - Banco de Dados

## **Por que SQLite?** - Apesar de ser solicitacao do desafio proposto, gostei da ideia

- **Simplicidade**: Arquivo único, sem necessidade de servidor
- **Portabilidade**: Funciona em qualquer ambiente
- **Performance**: Adequado para aplicações pequenas/médias e testes de manipulação de informação em banco
- **Zero Configuração**: Não precisa de instalação adicional
- **Requisito do Desafio**: Especificado no enunciado

### **SQLAlchemy** - ORM

**Por que SQLAlchemy?**

- **Maturidade**: ORM mais maduro do Python
- **Flexibilidade**: Permite SQL nativo quando necessário
- **Type Safety**: Integração com type hints
- **Migrations**: Suporte a versionamento de schema
- **Performance**: Query builder otimizado

### **Pydantic** - Validação de Dados

## **Por que Pydantic?** - a mágica para validar dados de uma forma perfomatica!

- **Validação Automática**: Valida tipos automaticamente
- **Serialização**: Converte objetos Python para JSON
- **Documentação**: Gera documentação automática
- **Performance**: Validação rápida com Rust (v2)
- **Integração**: Funciona perfeitamente com FastAPI

---

## Sistema de Autenticação

### **JWT (JSON Web Tokens)**

**Por que JWT?**

- **Stateless**: Não precisa armazenar sessões no servidor
- **Escalabilidade**: Funciona bem com múltiplos servidores
- **Segurança**: Tokens assinados digitalmente
- **Padrão da Indústria**: Amplamente adotado
- **Flexibilidade**: Pode conter informações customizadas

### **Bcrypt** - Hash de Senhas

**Por que Bcrypt?**

- **Segurança**: Algoritmo resistente a ataques de força bruta
- **Salt Automático**: Gera salt único para cada senha
- **Adaptativo**: Pode aumentar a complexidade conforme hardware evolui
- **Padrão**: Amplamente aceito na indústria
- **Biblioteca**: `passlib` com suporte a múltiplos algoritmos

### **Estrutura do Token**

```python
{
    "sub": "nome_usuario",  # Subject (quem é o usuário)
    "exp": 1234567890,      # Expiration (quando expira)
    "iat": 1234567890       # Issued At (quando foi criado)
}
```

---

## Estrutura de Pastas e Organização

```
desafio_api/
├── backend/
│   ├── models.py              # Entidades do banco
│   ├── database.py            # Configuração do banco
│   ├── routers/               # Rota dos endpoints
│   │   ├── auth.py           # Autenticação
│   │   └── documentos.py     # CRUD de documentos
│   ├── schemas/              # Validação de dados
│   │   ├── usuario.py        # Schemas de usuário
│   │   └── documento.py      # Schemas de documento
│   └── services/             # Lógica de negócio
│       ├── servico_autenticacao.py
│       ├── servico_usuario.py
│       └── servico_documento.py
├── main.py                   # Aplicação principal
├── pyproject.toml           # Dependências (Poetry)
└── docker-compose.yml       # Containerização
```

### **Por que esta organização?**

1. **Separação por Responsabilidade**: Cada pasta tem um propósito específico
2. **Facilita Navegação**: Desenvolvedores encontram código rapidamente
3. **Escalabilidade**: Fácil adicionar novos módulos
4. **Padrão da Indústria**: Estrutura reconhecida pela comunidade
5. **Manutenibilidade**: Mudanças ficam isoladas em suas respectivas pastas

---

## Fluxo de Dados e Processamento

### **1. Upload de PDF**

```
Cliente → Router → Service → PyPDF2 → Database
   ↓        ↓        ↓         ↓         ↓
  PDF    Validação  Extração  Processo  Persistência
```

### **2. Autenticação**

```
Login → Validação → Hash Check → JWT → Response
  ↓        ↓           ↓         ↓        ↓
Credenciais  Usuário  Senha   Token   Acesso
```

### **3. CRUD de Documentos**

```
Request → Router → Service → Database → Response
   ↓        ↓        ↓         ↓          ↓
  JSON   Validação  Lógica   Query    JSON
```

---

##  Segurança Implementada

### **1. Autenticação JWT**

- Tokens com expiração (30 minutos)
- Chave secreta para assinatura
- Validação em todas as rotas protegidas

### **2. Hash de Senhas**

- Bcrypt com salt automático
- Senhas nunca armazenadas em texto plano
- Verificação segura no login

### **3. Validação de Dados**

- Pydantic valida todos os inputs
- Sanitização automática de dados
- Prevenção de injeção de dados maliciosos

### **4. CORS Configurado**

- Headers apropriados para requisições cross-origin
- Configuração flexível para desenvolvimento

---

##  Processamento de PDFs

### **PyPDF2** - Biblioteca de Extração

**Por que PyPDF2?**

- **Simplicidade**: API fácil de usar
- **Confiabilidade**: Biblioteca madura e estável
- **Performance**: Adequada para PDFs simples
- **Compatibilidade**: Funciona com a maioria dos PDFs
- **Leveza**: Dependência pequena

### **Limitações Conhecidas**

- PDFs com imagens: Extrai apenas texto
- PDFs escaneados: Precisa de OCR
- Formatação complexa: Pode perder estrutura
- PDFs protegidos: Não consegue extrair

### **Fluxo de Processamento**

```python
def processar_upload_pdf(arquivo: UploadFile) -> Tuple[str, int]:
    # 1. Validar se é PDF
    if not validar_arquivo_pdf(arquivo):
        raise HTTPException(400, "Apenas arquivos PDF são aceitos")

    # 2. Ler conteúdo
    conteudo = arquivo.file.read()
    tamanho = len(conteudo)

    # 3. Extrair texto
    texto = extrair_texto_pdf(conteudo)

    # 4. Validar extração
    if not texto:
        raise HTTPException(400, "Não foi possível extrair texto")

    return texto, tamanho
```

---

## Performance e Otimizações

### **1. Operações Assíncronas**

- FastAPI com `async/await`
- Não bloqueia o servidor durante I/O
- Melhor throughput de requisições

### **2. Validação Eficiente**

- Pydantic com validação em C (v2)
- Validação apenas nos pontos de entrada
- Schemas reutilizáveis

### **3. Queries Otimizadas**

- Índices nas colunas de busca
- Filtros por usuário (segurança)
- Paginação para listas grandes

### **4. Gerenciamento de Memória**

- Processamento de PDF em chunks
- Liberação automática de recursos
- Upload limitado por tamanho

---

## Testabilidade e Qualidade

### **1. Separação de Responsabilidades**

- Services testáveis independentemente
- Mocks fáceis de implementar
- Testes unitários isolados

### **2. Injeção de Dependência**

- FastAPI com `Depends()`
- Fácil substituição de dependências
- Testes com mocks

### **3. Validação de Dados**

- Pydantic valida automaticamente
- Menos bugs de validação
- Documentação automática

---

## Escalabilidade e Manutenibilidade

### **1. Arquitetura Modular**

- Fácil adicionar novos endpoints
- Services reutilizáveis
- Baixo acoplamento entre módulos

### **2. Configuração Flexível**

- Variáveis de ambiente
- Configuração por ambiente
- Fácil deploy em diferentes ambientes

### **3. Logging e Monitoramento**

- Logs estruturados
- Rastreamento de erros
- Métricas de performance

---

## Melhorias Futuras

### **1. Banco de Dados**

- Migração para PostgreSQL em produção
- Connection pooling
- Replicação para alta disponibilidade

### **2. Processamento de PDF**

- Suporte a OCR para PDFs escaneados
- Extração de metadados
- Processamento em background

### **3. Segurança**

- Rate limiting
- Logs de auditoria
- Criptografia de dados sensíveis

### **4. Performance**

- Cache com Redis
- CDN para arquivos estáticos
- Load balancing

---

## Lições Aprendidas

### **1. Arquitetura**

- Service Layer Pattern é excelente para APIs
- Separação de responsabilidades facilita manutenção
- FastAPI + Pydantic é uma combinação poderosa

### **2. Segurança**

- JWT é ideal para APIs stateless
- Bcrypt é suficiente para hash de senhas
- Validação de dados é crucial

### **3. Desenvolvimento**

- Type hints melhoram muito a experiência
- Documentação automática economiza tempo
- Testes são essenciais para qualidade

### **4. Deploy**

- Docker facilita deployment
- SQLite é ótimo para desenvolvimento
- Poetry gerencia dependências muito bem

---

## Conclusão

Esta API foi desenvolvida seguindo **boas práticas da indústria** e **padrões arquiteturais reconhecidos**. A escolha de tecnologias foi baseada em:

1. **Requisitos do Desafio**: FastAPI + SQLite
2. **Performance**: Tecnologias modernas e otimizadas
3. **Manutenibilidade**: Código limpo e bem estruturado
4. **Segurança**: Práticas de segurança implementadas
5. **Escalabilidade**: Arquitetura preparada para crescimento

O projeto demonstra competência em:

- **Desenvolvimento de APIs RESTful**
- **Arquitetura de software**
- **Segurança de aplicações**
- **Processamento de documentos**
- **Boas práticas de desenvolvimento**

Esta base sólida permite evolução e adaptação conforme necessidades futuras, mantendo sempre a qualidade e performance da aplicação.
