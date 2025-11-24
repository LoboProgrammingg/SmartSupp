# Testes Unitários e de Integração

## 📋 Visão Geral

Esta documentação descreve a estrutura de testes implementada para o SmartSupp:
- **Testes Unitários**: Nodes do LangGraph, schemas Pydantic
- **Testes de Integração**: Endpoints da API, fluxo completo do agente
- **Coverage**: Configurado para mínimo de 70%

---

## 🏗️ Estrutura de Testes

```
tests/
├── __init__.py
├── conftest.py                      # Fixtures compartilhadas
├── unit/
│   ├── __init__.py
│   ├── test_nodes.py                # Testes dos nodes LangGraph
│   └── test_schemas.py              # Testes dos schemas Pydantic
└── integration/
    ├── __init__.py
    ├── test_api_endpoints.py        # Testes dos endpoints da API
    └── test_agent_flow.py           # Testes do fluxo completo do agente
```

---

## 📚 Componentes Testados

### 1. Fixtures (`tests/conftest.py`)

#### Database Fixtures

**`test_engine`**
- Engine de teste para criar banco
- Escopo: session (compartilhado por todos os testes)

**`setup_test_db`**
- Cria schema de teste no início
- Remove schema no final
- Escopo: session, autouse=True

**`test_session`**
- Sessão de teste isolada por teste
- Rollback automático após cada teste
- Escopo: function

#### Data Fixtures

**`sample_tenant`**
- Tenant de teste com `plan=PRO`

**`sample_user_profile`**
- Perfil de usuário completo:
  - Biometria (75.5kg, 175cm, 30 anos, male)
  - Goal: MUSCLE_GAIN
  - Restrições: LACTOSE_FREE
  - Condições: DIABETES
  - Budget: MEDIUM

**`sample_scientific_data`**
- Dados científicos (Whey Protein, STRONG evidence)

**`sample_products`**
- 2 produtos de teste:
  - Growth Whey Protein
  - IntegralMedica Whey Zero Lactose

**`test_client`**
- Cliente de teste FastAPI (TestClient)

---

### 2. Testes Unitários

#### Testes dos Nodes LangGraph (`tests/unit/test_nodes.py`)

**`test_anamnesis_collector_with_profile`**
- Testa coleta de anamnese com perfil existente
- Verifica que dados do perfil são carregados corretamente

**`test_anamnesis_collector_without_profile`**
- Testa validação de campos sem perfil
- Verifica que campos obrigatórios são validados

**`test_anamnesis_collector_missing_fields`**
- Testa tratamento de campos faltando
- Verifica que erros são retornados adequadamente

**`test_science_retriever`**
- Testa busca de dados científicos
- Verifica mapeamento goal → categoria
- Verifica filtro por evidência STRONG

**`test_science_retriever_no_goal`**
- Testa tratamento de erro sem goal definido

**`test_comparative_analysis`**
- Testa análise comparativa completa
- Verifica filtros por restrições/condições
- Verifica ranqueamento de produtos

---

#### Testes dos Schemas (`tests/unit/test_schemas.py`)

**`test_chat_request_valid`**
- Testa ChatRequest com todos os campos

**`test_chat_request_minimal`**
- Testa ChatRequest com apenas campo obrigatório

**`test_biometrics_input_valid`**
- Testa BiometricsInput com dados válidos

**`test_biometrics_input_invalid_weight`**
- Testa validação: peso deve ser > 0

**`test_biometrics_input_invalid_age`**
- Testa validação: idade deve ser <= 120

**`test_biometrics_input_invalid_sex`**
- Testa validação: sexo deve ser male|female|other

**`test_user_profile_create_valid`**
- Testa UserProfileCreate com dados válidos

**`test_user_profile_update_all_optional`**
- Testa UserProfileUpdate (todos campos opcionais)

**`test_brand_performance_response`**
- Testa BrandPerformanceResponse

---

### 3. Testes de Integração

#### Testes dos Endpoints da API (`tests/integration/test_api_endpoints.py`)

**`test_create_user_profile`**
- POST /user-profile
- Verifica criação de perfil
- Verifica cálculo de BMI

**`test_get_user_profile`**
- GET /user-profile/{id}
- Verifica busca de perfil existente

**`test_update_user_profile`**
- PUT /user-profile/{id}
- Verifica atualização de perfil

**`test_chat_endpoint`**
- POST /chat
- Testa fluxo completo do agente via API
- Verifica resposta gerada

**`test_chat_endpoint_without_profile`**
- POST /chat sem perfil
- Verifica tratamento de erro

**`test_analytics_brand_performance`**
- GET /analytics/brand-performance
- Verifica agregação de dados

**`test_get_user_profile_not_found`**
- GET /user-profile/{id} inexistente
- Verifica retorno 404

**`test_create_user_profile_invalid_data`**
- POST /user-profile com dados inválidos
- Verifica retorno 422 (validation error)

---

#### Testes do Fluxo do Agente (`tests/integration/test_agent_flow.py`)

**`test_agent_complete_flow`**
- Testa execução completa do agente
- Verifica todos os steps
- Verifica que dados são coletados e processados

**`test_agent_without_profile`**
- Testa agente sem perfil de usuário
- Verifica processamento com dados básicos

**`test_agent_error_handling`**
- Testa tratamento de erros
- Verifica que erros não quebram o fluxo

---

## 🚀 Como Executar

### Pré-requisitos

1. **Banco de Teste**
```bash
# Criar banco de teste
createdb smartsupp_test

# Ou via docker-compose (adicionar serviço de teste)
```

2. **Variáveis de Ambiente**
```env
# Para testes, usar banco separado
TEST_DATABASE_URL=postgresql+asyncpg://test:test@localhost:5432/smartsupp_test
```

### Executar Todos os Testes

```bash
# Via Poetry
poetry run pytest

# Com coverage
poetry run pytest --cov=src --cov-report=html

# Com verbose
poetry run pytest -v
```

### Executar por Categoria

```bash
# Apenas testes unitários
poetry run pytest tests/unit/

# Apenas testes de integração
poetry run pytest tests/integration/

# Apenas testes de nodes
poetry run pytest tests/unit/test_nodes.py

# Apenas testes de schemas
poetry run pytest tests/unit/test_schemas.py

# Apenas testes de API
poetry run pytest tests/integration/test_api_endpoints.py
```

### Executar Teste Específico

```bash
# Por nome
poetry run pytest tests/unit/test_nodes.py::test_anamnesis_collector_with_profile

# Por pattern
poetry run pytest -k "test_anamnesis"

# Por marcador
poetry run pytest -m "asyncio"
```

### Ver Coverage

```bash
# Terminal
poetry run pytest --cov=src --cov-report=term-missing

# HTML (abre em navegador)
poetry run pytest --cov=src --cov-report=html
open htmlcov/index.html

# XML (para CI/CD)
poetry run pytest --cov=src --cov-report=xml
```

---

## 📊 Coverage

### Configuração

**Mínimo**: 70% (configurado no `pyproject.toml`)

```toml
[tool.pytest.ini_options]
cov_fail_under = 70
```

### Relatórios

- **Terminal**: Mostra linhas não cobertas
- **HTML**: Relatório interativo
- **XML**: Para integração CI/CD

---

## 🔍 Exemplos de Testes

### Exemplo 1: Teste Unitário

```python
@pytest.mark.asyncio
async def test_anamnesis_collector_with_profile(test_session, sample_user_profile):
    """Testa AnamnesisCollector com perfil existente"""
    state: AgentState = {
        "session_id": "test-session",
        "tenant_id": sample_user_profile.tenant_id,
        "user_profile_id": sample_user_profile.id,
        # ... outros campos
    }
    
    config = {"configurable": {"session": test_session}}
    result = await anamnesis_collector(state, config)
    
    assert result["step"] == "anamnesis_collected_from_profile"
    assert result["goal"] == UserGoal.MUSCLE_GAIN.value
```

### Exemplo 2: Teste de Integração

```python
@pytest.mark.asyncio
async def test_create_user_profile(test_client: TestClient, sample_tenant):
    """Testa criação de perfil de usuário"""
    response = test_client.post(
        "/user-profile",
        headers={"X-Tenant-ID": str(sample_tenant.id)},
        json={
            "biometrics": {
                "weight_kg": 75.5,
                "height_cm": 175,
                "age": 30,
                "sex": "male",
            },
            "goal": "muscle_gain",
            # ... outros campos
        },
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["goal"] == "muscle_gain"
```

---

## 🛠️ Troubleshooting

### Problema: Banco de teste não existe

**Solução:**
```bash
createdb smartsupp_test
```

### Problema: Fixtures não são encontradas

**Solução:**
- Verificar que `conftest.py` está na raiz de `tests/`
- Verificar imports corretos

### Problema: Testes assíncronos falham

**Solução:**
- Verificar que `@pytest.mark.asyncio` está presente
- Verificar que `asyncio_mode = "auto"` no `pyproject.toml`

### Problema: Coverage abaixo do mínimo

**Solução:**
- Adicionar mais testes
- Verificar linhas não cobertas com `--cov-report=term-missing`
- Cobrir casos de erro e edge cases

---

## 📝 Boas Práticas Implementadas

### 1. Isolamento
- Cada teste é independente
- Rollback automático após cada teste
- Fixtures isoladas

### 2. Fixtures Reutilizáveis
- Fixtures compartilhadas em `conftest.py`
- Dados de teste consistentes
- Setup/teardown automático

### 3. Cobertura
- Mínimo de 70%
- Foco em casos de sucesso e erro
- Edge cases cobertos

### 4. Nomenclatura
- Nomes descritivos (`test_*`)
- Docstrings explicando o que cada teste faz
- Organização por categoria

### 5. Assertions Claros
- Assertions específicos
- Mensagens de erro úteis
- Verificação de múltiplos aspectos

---

## ✅ Checklist de Testes

### Testes Unitários
- [x] Nodes LangGraph testados
- [x] Schemas Pydantic testados
- [x] Validações testadas
- [x] Casos de erro testados

### Testes de Integração
- [x] Endpoints da API testados
- [x] Fluxo completo do agente testado
- [x] Isolamento multitenant testado
- [x] Tratamento de erros testado

### Infraestrutura
- [x] Pytest configurado
- [x] Coverage configurado
- [x] Fixtures criadas
- [x] Banco de teste configurado

---

## 📚 Referências

- **Pytest**: https://docs.pytest.org/
- **Pytest-asyncio**: https://pytest-asyncio.readthedocs.io/
- **Pytest-cov**: https://pytest-cov.readthedocs.io/
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/

---

**Branch**: `feature/tests`  
**Status**: ✅ Completa e pronta para merge

