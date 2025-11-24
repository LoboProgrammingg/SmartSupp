# Etapa 5: API e Dashboard Data

## 📋 Visão Geral

Esta etapa implementa a **API REST completa** com FastAPI, integrando todos os componentes anteriores:
- **POST /chat** - Endpoint principal para consultas e recomendações
- **POST /user-profile** - Criar perfil de usuário
- **GET /user-profile/{id}** - Buscar perfil de usuário
- **PUT /user-profile/{id}** - Atualizar perfil de usuário
- **GET /analytics/brand-performance** - Analytics de performance de marcas

---

## 🏗️ Arquitetura Implementada

### Estrutura de Pastas

```
src/api/
├── __init__.py
├── schemas.py                 # Schemas Pydantic (requests/responses)
├── dependencies.py            # Dependencies FastAPI
└── routes/
    ├── __init__.py
    ├── chat.py                # Rotas de chat/recomendação
    ├── user_profile.py        # Rotas de perfil de usuário
    └── analytics.py           # Rotas de analytics

src/main.py                    # FastAPI app principal (atualizado)
```

---

## 📚 Componentes Implementados

### 1. Schemas Pydantic (`src/api/schemas.py`)

#### ChatRequest / ChatResponse

**ChatRequest:**
- `user_input`: Input do usuário (obrigatório)
- `user_profile_id`: ID do perfil (opcional)
- `session_id`: ID da sessão (opcional)

**ChatResponse:**
- `response`: Resposta gerada pelo agente
- `explanation`: Explicação detalhada
- `recommended_product_ids`: IDs dos produtos recomendados
- `ranking_data`: Dados de ranqueamento
- `session_id`: ID da sessão
- `step`: Último step executado

#### UserProfile Schemas

**BiometricsInput:**
- `weight_kg`: Peso em kg (> 0)
- `height_cm`: Altura em cm (> 0)
- `age`: Idade em anos (0 < age <= 120)
- `sex`: Sexo (male|female|other)

**UserProfileCreate:**
- `biometrics`: Dados biométricos
- `goal`: Enum `UserGoal`
- `dietary_restrictions`: Lista de `DietaryRestriction`
- `medical_conditions`: Lista de `MedicalCondition`
- `budget_range`: Enum `BudgetRange`

**UserProfileUpdate:**
- Todos os campos opcionais (PATCH-style)

**UserProfileResponse:**
- Todos os campos do perfil com timestamps

#### Analytics Schemas

**BrandPerformanceResponse:**
- `brand_name`: Nome da marca
- `product_name`: Nome do produto
- `recommendation_count`: Quantidade de recomendações
- `avg_satisfaction`: Score médio de satisfação
- `total_selections`: Total de seleções
- `conversion_rate`: Taxa de conversão (selections / recommendations)

**AnalyticsResponse:**
- `tenant_id`: ID do tenant
- `period_start`: Início do período
- `period_end`: Fim do período
- `total_interactions`: Total de interações
- `brand_performance`: Lista de performance por marca

---

### 2. Dependencies (`src/api/dependencies.py`)

#### `get_db_session()`
- Dependency para sessão de banco assíncrona
- Usa `get_session()` do core/database.py
- Gerencia ciclo de vida da sessão automaticamente

#### `get_tenant_id_from_header()`
- Extrai `tenant_id` do header `X-Tenant-ID`
- Para desenvolvimento/teste (em produção usar JWT)
- Em modo DEBUG, usa tenant demo padrão (ID 1)
- Define escopo de tenant via `TenantScope.set_tenant()`

**Uso:**
```python
tenant_id: int = Depends(get_tenant_id_from_header)
```

---

### 3. Rotas da API

#### POST /chat (`src/api/routes/chat.py`)

**Endpoint**: `POST /chat`

**Request Body:**
```json
{
  "user_input": "Qual whey protein é melhor para mim?",
  "user_profile_id": 1,
  "session_id": "optional-session-id"
}
```

**Response (200 OK):**
```json
{
  "response": "Recomendo Growth Whey Protein...",
  "explanation": "Baseado nas evidências científicas...",
  "recommended_product_ids": [1, 3, 5],
  "ranking_data": {
    "1": {
      "score": 95.5,
      "reasons": ["Alto teor de proteína", "Bom custo-benefício"],
      "match_score": 0.955
    }
  },
  "session_id": "uuid-session-id",
  "step": "analytics_logged"
}
```

**Funcionalidade:**
1. Recebe input do usuário
2. Executa agente LangGraph completo
3. Retorna resposta gerada com produtos recomendados
4. Salva interação para BI automaticamente

---

#### POST /user-profile (`src/api/routes/user_profile.py`)

**Endpoint**: `POST /user-profile`

**Request Body:**
```json
{
  "biometrics": {
    "weight_kg": 75.5,
    "height_cm": 175,
    "age": 30,
    "sex": "male"
  },
  "goal": "muscle_gain",
  "dietary_restrictions": ["lactose_free"],
  "medical_conditions": ["diabetes"],
  "budget_range": "medium"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "tenant_id": 1,
  "biometrics": {
    "weight_kg": 75.5,
    "height_cm": 175,
    "age": 30,
    "sex": "male",
    "bmi": 24.7
  },
  "goal": "muscle_gain",
  "dietary_restrictions": ["lactose_free"],
  "medical_conditions": ["diabetes"],
  "budget_range": "medium",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

**Funcionalidade:**
- Cria novo perfil de usuário
- Calcula BMI automaticamente
- Valida dados com Pydantic
- Isola por tenant automaticamente

---

#### GET /user-profile/{profile_id}

**Endpoint**: `GET /user-profile/{profile_id}`

**Response (200 OK):**
- Mesmo formato do POST, mas busca perfil existente

**Funcionalidade:**
- Busca perfil por ID
- Verifica isolamento de tenant
- Retorna 404 se não encontrado

---

#### PUT /user-profile/{profile_id}

**Endpoint**: `PUT /user-profile/{profile_id}`

**Request Body:**
- Mesmo formato do POST, mas todos os campos são opcionais (PATCH-style)

**Response (200 OK):**
- Perfil atualizado

**Funcionalidade:**
- Atualiza perfil existente
- Recalcula BMI se biometrics for atualizado
- Valida isolamento de tenant

---

#### GET /analytics/brand-performance (`src/api/routes/analytics.py`)

**Endpoint**: `GET /analytics/brand-performance?days=30`

**Query Parameters:**
- `days`: Período em dias (1-365, padrão: 30)

**Response (200 OK):**
```json
{
  "tenant_id": 1,
  "period_start": "2024-01-01T00:00:00Z",
  "period_end": "2024-01-31T23:59:59Z",
  "total_interactions": 150,
  "brand_performance": [
    {
      "brand_name": "Growth Supplements",
      "product_name": "Whey Protein Concentrado",
      "recommendation_count": 45,
      "avg_satisfaction": 4.5,
      "total_selections": 20,
      "conversion_rate": 0.4444
    },
    {
      "brand_name": "Max Titanium",
      "product_name": "Whey 3W - Blend",
      "recommendation_count": 30,
      "avg_satisfaction": 3.8,
      "total_selections": 10,
      "conversion_rate": 0.3333
    }
  ]
}
```

**Funcionalidade:**
- Agrega interações do período
- Calcula recomendações por produto
- Calcula taxa de conversão (seleções / recomendações)
- Calcula score médio de satisfação
- Ordena por quantidade de recomendações

---

### 4. Integração com Main (`src/main.py`)

**Atualizações:**
- Importa rotas de `src.api.routes`
- Registra rotas via `app.include_router()`
- Adiciona middleware para limpar escopo de tenant após requisição

**Middleware de Tenant:**
```python
@app.middleware("http")
async def tenant_middleware(request, call_next):
    response = await call_next(request)
    TenantScope.clear_tenant()  # Limpa escopo após requisição
    return response
```

---

## 🔧 Configuração

### Variáveis de Ambiente

Nenhuma nova variável de ambiente necessária. Usa as mesmas da Etapa 1:
- `POSTGRES_*`: Database
- `SECRET_KEY`: Security
- `GOOGLE_*`: LLM (Gemini)

---

## 🚀 Como Usar

### 1. Iniciar API

```bash
# Via Poetry
poetry run dev

# Ou diretamente
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Acessar Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Testar Endpoints

#### Criar Perfil

```bash
curl -X POST "http://localhost:8000/user-profile" \
  -H "X-Tenant-ID: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "biometrics": {
      "weight_kg": 75.5,
      "height_cm": 175,
      "age": 30,
      "sex": "male"
    },
    "goal": "muscle_gain",
    "dietary_restrictions": ["lactose_free"],
    "medical_conditions": ["diabetes"],
    "budget_range": "medium"
  }'
```

#### Fazer Consulta

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "X-Tenant-ID: 1" \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Qual whey protein é melhor para mim?",
    "user_profile_id": 1
  }'
```

#### Ver Analytics

```bash
curl -X GET "http://localhost:8000/analytics/brand-performance?days=30" \
  -H "X-Tenant-ID: 1"
```

---

## 📊 Documentação Swagger

A API inclui documentação Swagger automática em `/docs`:

- **Schemas**: Todos os schemas Pydantic documentados
- **Endpoints**: Todos os endpoints com exemplos
- **Try it out**: Teste direto na UI

---

## 🔍 Exemplos de Respostas

### POST /chat

**Sucesso (200 OK):**
```json
{
  "response": "Recomendo Growth Whey Protein Concentrado...",
  "explanation": "Baseado nas evidências científicas...",
  "recommended_product_ids": [1, 3, 5],
  "ranking_data": {...},
  "session_id": "uuid",
  "step": "analytics_logged"
}
```

**Erro (500):**
```json
{
  "detail": "Erro ao processar requisição: ..."
}
```

---

## 🎯 Fluxo Completo

### 1. Usuário Cria Perfil

```
POST /user-profile
  → Cria UserProfile
  → Calcula BMI
  → Retorna perfil criado
```

### 2. Usuário Faz Consulta

```
POST /chat
  → Extrai tenant_id do header
  → Busca perfil (se user_profile_id fornecido)
  → Executa agente LangGraph:
     1. AnamnesisCollector
     2. ScienceRetriever
     3. ComparativeAnalysis
     4. ResponseGenerator
     5. AnalyticsLogger
  → Retorna resposta
```

### 3. Visualizar Analytics

```
GET /analytics/brand-performance
  → Agrega interações do período
  → Calcula métricas por produto
  → Retorna performance de marcas
```

---

## 📝 Boas Práticas Implementadas

### 1. Validação com Pydantic
- Todos os inputs validados
- Type hints completos
- Mensagens de erro claras

### 2. Isolamento Multitenant
- Header `X-Tenant-ID` (dev/test)
- Verificação em todas as queries
- Middleware para limpar escopo

### 3. Error Handling
- HTTPExceptions apropriadas
- Códigos de status corretos
- Mensagens de erro claras

### 4. Documentação
- Swagger automático
- Docstrings em todos os endpoints
- Schemas documentados

### 5. Clean Code
- Código limpo e legível
- Funções pequenas e focadas
- Reutilização de dependencies

---

## 🔒 Segurança

### Em Produção

**Usar JWT ao invés de header:**
```python
# Em produção, substituir get_tenant_id_from_header por:
from src.core.security import get_current_tenant_id

tenant_id: int = Depends(get_current_tenant_id)
```

**Configurar CORS:**
```python
# Atualizar em main.py:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.smartsupp.com"],  # Origins específicos
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)
```

---

## ✅ Checklist da Etapa 5

- [x] Schemas Pydantic criados
- [x] Dependencies implementadas
- [x] POST /chat endpoint implementado
- [x] POST /user-profile endpoint implementado
- [x] GET /user-profile/{id} endpoint implementado
- [x] PUT /user-profile/{id} endpoint implementado
- [x] GET /analytics/brand-performance endpoint implementado
- [x] Integração com agente LangGraph
- [x] Middleware para limpar escopo de tenant
- [x] Rotas registradas no main.py
- [x] Documentação Swagger automática
- [x] Código limpo, PEP8, type hints
- [x] Documentação completa criada
- [x] Todos os commits incrementais realizados

---

## 📚 Referências

- **FastAPI**: https://fastapi.tiangolo.com/
- **Pydantic**: https://docs.pydantic.dev/
- **Swagger UI**: https://swagger.io/tools/swagger-ui/
- **ReDoc**: https://github.com/Redocly/redoc

---

**Branch**: `feature/etapa-5-api`  
**Status**: ✅ Completa e pronta para merge

