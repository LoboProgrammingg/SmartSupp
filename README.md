# SmartSupp 🏋️‍♂️

SaaS Multitenant de Recomendação de Suplementos Esportivos

## 🎯 Visão Geral

Plataforma B2B SaaS que utiliza IA (Gemini 2.5 Flash) para recomendar suplementos esportivos personalizados, considerando:
- Dados vitais e objetivos do usuário
- Base científica global (AIS/Examine)
- Estoque e marcas disponíveis por tenant
- Comparação técnica detalhada entre produtos

## 🏗️ Arquitetura

- **Backend**: FastAPI (Async)
- **Database**: PostgreSQL com SQLModel
- **AI**: LangGraph + Google Gemini 2.5 Flash
- **ORM**: SQLModel + Alembic
- **Multitenancy**: Isolamento via `tenant_id` em todas as tabelas de negócio

## 🚀 Quick Start

### 1. Pré-requisitos

```bash
# Instalar Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Instalar Docker e Docker Compose
# Ver: https://docs.docker.com/get-docker/
```

### 2. Configuração

```bash
# Copiar variáveis de ambiente
cp .env.example .env

# Editar .env com suas credenciais
nano .env
```

### 3. Iniciar Infraestrutura

```bash
# Subir PostgreSQL
docker-compose up -d

# Verificar status
docker-compose ps
```

### 4. Instalar Dependências

```bash
# Instalar dependências do Poetry
poetry install

# Ativar ambiente virtual
poetry shell
```

### 5. Rodar Aplicação

```bash
# Desenvolvimento
poetry run dev

# Ou via uvicorn direto
uvicorn src.main:app --reload
```

## 📁 Estrutura do Projeto (DDD)

```
smartsupp/
├── src/
│   ├── core/              # Infraestrutura (DB, Security, Config)
│   ├── domain/            # Entidades de Domínio
│   ├── application/       # Casos de Uso e Services
│   ├── infrastructure/    # Repositories e Integrações Externas
│   ├── api/               # FastAPI Routes e Dependencies
│   └── agents/            # LangGraph Agents
├── tests/
├── alembic/               # Migrations
├── scripts/               # Scripts de seeding
├── pyproject.toml
├── docker-compose.yml
└── .env
```

## 🔐 Estratégia Multitenant

### Isolamento de Dados

- Todas as tabelas de negócio possuem coluna `tenant_id`
- `TenantScope` gerencia o contexto de tenant por requisição
- Middleware e Dependencies garantem isolamento automático
- `ScientificData` é **global** (sem tenant_id)

### Autenticação

- JWT tokens contêm `tenant_id` no payload
- Middleware extrai tenant do header `X-Tenant-ID` (dev/test)
- Dependencies (`get_current_tenant_id`) garantem escopo correto

## 📝 Roadmap

- [x] **Etapa 1**: Infraestrutura e Arquitetura Multitenant
- [ ] **Etapa 2**: Modelagem de Dados (PostgreSQL)
- [ ] **Etapa 3**: Ingestão de Conhecimento (Seeding)
- [ ] **Etapa 4**: O Cérebro (LangGraph + Gemini)
- [ ] **Etapa 5**: API e Dashboard

## 🔗 Links

- Repositório: https://github.com/LoboProgrammingg/SmartSupp
- Documentação da API: http://localhost:8000/docs (após iniciar)

## 📄 Licença

Proprietário - LoboProgramming

