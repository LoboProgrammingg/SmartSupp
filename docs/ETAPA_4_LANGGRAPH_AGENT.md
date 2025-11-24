# Etapa 4: O Cérebro (LangGraph + Gemini 2.5 Flash)

## 📋 Visão Geral

Esta etapa implementa o **agente inteligente** que realiza o **Core Loop** completo de recomendação:
1. **Anamnesis**: Coleta dados do usuário
2. **Science**: Consulta base científica (AIS/Examine)
3. **Inventory & Brands**: Consulta estoque do tenant
4. **Matchmaking**: Compara e ranqueia produtos
5. **Response**: Gera explicação comparativa personalizada
6. **Analytics**: Salva interação para BI

---

## 🏗️ Arquitetura Implementada

### Estrutura de Pastas

```
src/agents/
├── state.py                  # AgentState (TypedDict) - estado do agente
├── graph.py                  # Grafo LangGraph - orquestração de nodes
├── runner.py                 # Runner do agente - execução completa
├── utils.py                  # Utilitários (get_session_from_config)
└── nodes/
    ├── anamnesis_collector.py    # Node 1: Coleta anamnese
    ├── science_retriever.py      # Node 2: Busca dados científicos
    ├── comparative_analysis.py   # Node 3: Análise comparativa (matchmaking)
    ├── response_generator.py     # Node 4: Gera resposta com Gemini 2.5
    └── analytics_logger.py       # Node 5: Salva para BI

src/infrastructure/llm/
└── gemini.py                 # Integração Gemini 2.5 Flash (Vertex AI / Google AI Studio)
```

### Fluxo do Agente

```
┌─────────────────────┐
│   AnamnesisCollector│
│   (Coleta dados)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  ScienceRetriever   │
│  (Busca científica) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ ComparativeAnalysis │
│   (Matchmaking)     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ ResponseGenerator   │
│  (Gemini 2.5 Flash) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  AnalyticsLogger    │
│     (Salva BI)      │
└──────────┬──────────┘
           │
           ▼
          END
```

---

## 📚 Componentes Implementados

### 1. AgentState (`src/agents/state.py`)

**TypedDict** que define o estado do agente durante todo o fluxo.

**Campos Principais:**
- `session_id`: ID da sessão
- `tenant_id`: ID do tenant (multitenancy)
- `user_profile_id`: ID do perfil do usuário
- `user_input`: Input inicial do usuário
- `biometrics`, `goal`, `dietary_restrictions`, `medical_conditions`, `budget_range`: Dados de anamnese
- `scientific_data`: Dados científicos recuperados
- `recommended_category`: Categoria de suplemento recomendada
- `available_products`, `filtered_products`, `ranked_products`: Produtos em diferentes estágios
- `ranking_data`: Dados de ranqueamento (score, razões, match_score)
- `response`, `explanation`: Resposta gerada pelo LLM
- `recommended_product_ids`: IDs dos produtos recomendados (top 3)
- `errors`: Lista de erros (se houver)
- `step`: Nome do último step executado

---

### 2. Integração Gemini 2.5 Flash (`src/infrastructure/llm/gemini.py`)

**Suporte a dois modos:**

#### Modo 1: Vertex AI (Produção)
```python
# Requer no .env:
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
VERTEX_AI_LOCATION=us-central1
GEMINI_MODEL=gemini-2.0-flash-exp
```

#### Modo 2: Google AI Studio (Desenvolvimento/Teste)
```python
# Requer no .env:
GOOGLE_API_KEY=your-api-key
GEMINI_MODEL=gemini-2.0-flash-exp
```

**Função `get_llm()`**:
- Prioriza Vertex AI se configurado
- Fallback para Google AI Studio
- Retorna instância do LLM configurada

---

### 3. Nodes do LangGraph

#### Node 1: AnamnesisCollector (`src/agents/nodes/anamnesis_collector.py`)

**Responsabilidade**: Coleta e valida dados de anamnese.

**Lógica:**
1. Se `user_profile_id` existe, busca perfil do banco
2. Se não, valida campos obrigatórios no estado
3. Valida tipos e valores (enums)

**Campos Obrigatórios:**
- `biometrics`: Dict com peso, altura, idade, sexo, BMI
- `goal`: Enum `UserGoal` (muscle_gain, weight_loss, etc.)
- `budget_range`: Enum `BudgetRange` (low, medium, high, premium)

**Output:**
- Atualiza `state["biometrics"]`, `state["goal"]`, `state["dietary_restrictions"]`, etc.
- Define `state["step"] = "anamnesis_collected"`

---

#### Node 2: ScienceRetriever (`src/agents/nodes/science_retriever.py`)

**Responsabilidade**: Busca dados científicos baseado no objetivo do usuário.

**Mapeamento Objetivo → Categoria:**
```python
GOAL_TO_CATEGORY = {
    "muscle_gain": SupplementCategory.PROTEIN,
    "weight_loss": SupplementCategory.PROTEIN,
    "endurance": SupplementCategory.CAFFEINE,
    "sports_performance": SupplementCategory.CREATINE,
    "recovery": SupplementCategory.PROTEIN,
    "general_health": SupplementCategory.MULTIVITAMIN,
}
```

**Lógica:**
1. Determina categoria baseada no `goal`
2. Busca `ScientificData` com `evidence_level = STRONG` (apenas evidências fortes)
3. Filtra por categoria

**Output:**
- Atualiza `state["recommended_category"]`
- Define `state["scientific_data"]` com lista de dados científicos

---

#### Node 3: ComparativeAnalysis (`src/agents/nodes/comparative_analysis.py`)

**Responsabilidade**: Filtra e ranqueia produtos (Matchmaking).

**Filtros Aplicados:**

1. **Diabetes** → Remove produtos com `maltodextrin = True`
2. **Lactose Free** → Remove produtos com `no_lactose = False`
3. **Vegan** → Remove produtos com `vegan = False`
4. **Gluten Free** → Remove produtos com `no_gluten = False`
5. **No Artificial Sweeteners** → Remove produtos com `artificial_sweeteners = True`

**Sistema de Score (0-100):**

| Critério | Peso | Cálculo |
|----------|------|---------|
| Proteína | 40% | `(protein_g / 30) * 100` (max 100) |
| Custo-Benefício | 30% | `100 - (price_per_protein_g * 2)` |
| Certificações | 20% | `len(certifications) * 20` (max 100) |
| Pureza | 10% | Bônus por sem aditivos desnecessários |

**Cálculo de Custo-Benefício:**
```python
price_per_protein_g = product.price / nutritional_info["protein_g"]
# Menor preço por grama = maior score
```

**Output:**
- `state["available_products"]`: Todos os produtos disponíveis
- `state["filtered_products"]`: Produtos após filtros
- `state["ranked_products"]`: Produtos ranqueados por score
- `state["ranking_data"]`: Dict com score, razões, match_score por produto
- `state["recommended_product_ids"]`: Top 3 IDs

---

#### Node 4: ResponseGenerator (`src/agents/nodes/response_generator.py`)

**Responsabilidade**: Gera explicação comparativa usando Gemini 2.5 Flash.

**Prompt Template:**

```
System: Você é um especialista em suplementos esportivos que faz 
recomendações personalizadas baseadas em evidência científica.

User: Baseado nas seguintes informações, gere uma recomendação:

**Produtos Ranqueados:**
[Top 3 produtos com score, preço, razões]

**Contexto Científico:**
[Evidências científicas relevantes]

**Perfil do Usuário:**
[Condições médicas, restrições, objetivo]

Gere uma resposta que:
1. Recomende o melhor produto (top 1) e explique por quê
2. Compare com os outros produtos se relevante
3. Justifique considerando condições médicas, restrições e evidência científica
4. Seja claro, objetivo e profissional
```

**Fallback:**
Se LLM falhar, retorna resposta simples baseada nos scores e razões.

**Output:**
- `state["response"]`: Resposta completa gerada pelo LLM
- `state["explanation"]`: Mesma resposta (para compatibilidade)

---

#### Node 5: AnalyticsLogger (`src/agents/nodes/analytics_logger.py`)

**Responsabilidade**: Salva interação no banco para BI.

**Dados Salvos:**
- `tenant_id`: ID do tenant
- `user_profile_id`: ID do perfil (se houver)
- `session_id`: ID da sessão
- `query_text`: Texto da consulta
- `recommended_products`: Array de IDs recomendados
- `ranking_data`: Dados completos de ranqueamento (JSONB)
- `created_at`: Timestamp da interação

**Error Handling:**
- Erros não quebram o fluxo
- Logs de erro são salvos em `state["errors"]`

**Output:**
- `state["step"] = "analytics_logged"`

---

### 4. Grafo LangGraph (`src/agents/graph.py`)

**Função `create_graph()`**:
- Cria `StateGraph` com `AgentState`
- Adiciona todos os 5 nodes
- Define fluxo linear (entry → node1 → node2 → ... → END)
- Compila e retorna grafo

**Singleton Pattern:**
- Função `get_graph()` retorna instância singleton
- Evita recriar grafo a cada chamada

---

### 5. Runner do Agente (`src/agents/runner.py`)

**Função `run_agent()`**:

**Parâmetros:**
- `user_input`: Input do usuário
- `tenant_id`: ID do tenant (multitenancy)
- `user_profile_id`: ID do perfil (opcional)
- `session`: Sessão assíncrona do banco
- `session_id`: ID da sessão (opcional, gera UUID se não fornecido)

**Fluxo:**
1. Cria estado inicial (`AgentState`)
2. Obtém grafo compilado
3. Configura sessão no `config`
4. Executa grafo com `graph.ainvoke()`
5. Retorna estado final como dict

**Error Handling:**
- Captura exceções
- Retorna estado com erro e mensagem amigável

---

### 6. Utilitários (`src/agents/utils.py`)

**Função `get_session_from_config()`**:
- Extrai sessão do `config` do LangGraph
- Acessa `config["configurable"]["session"]`

**Uso nos Nodes:**
```python
session = get_session_from_config(config)
if session:
    # Usar sessão
```

---

## 🔧 Configuração

### Variáveis de Ambiente

#### Vertex AI (Produção)
```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
VERTEX_AI_LOCATION=us-central1
GEMINI_MODEL=gemini-2.0-flash-exp
```

#### Google AI Studio (Dev/Test)
```env
GOOGLE_API_KEY=your-api-key
GEMINI_MODEL=gemini-2.0-flash-exp
```

**Prioridade:**
1. Vertex AI (se `GOOGLE_CLOUD_PROJECT` e `GOOGLE_APPLICATION_CREDENTIALS` configurados)
2. Google AI Studio (se `GOOGLE_API_KEY` configurado)
3. Erro se nenhum configurado

---

## 🚀 Como Usar

### Exemplo Básico

```python
from src.agents.runner import run_agent
from src.core.database import get_session

async def recommend_supplement():
    async for session in get_session():
        result = await run_agent(
            user_input="Preciso de um whey protein para ganho de massa",
            tenant_id=1,
            user_profile_id=1,
            session=session,
        )
        
        print(result["response"])
        print(f"Produtos recomendados: {result['recommended_product_ids']}")
```

### Exemplo com Dados Customizados

```python
from src.domain.enums import UserGoal, BudgetRange, DietaryRestriction, MedicalCondition

result = await run_agent(
    user_input="Qual whey protein é melhor para mim?",
    tenant_id=1,
    user_profile_id=None,
    session=session,
)

# Ou passar dados diretamente no estado inicial (após ajustes no runner)
```

---

## 🎯 Exemplos de Casos de Uso

### Caso 1: Usuário Diabético

**Input:**
- Goal: `muscle_gain`
- Medical Conditions: `[diabetes]`
- Dietary Restrictions: `[]`

**Fluxo:**
1. **AnamnesisCollector**: Coleta dados
2. **ScienceRetriever**: Busca dados de proteína (AIS)
3. **ComparativeAnalysis**: Filtra produtos sem maltodextrina
   - ✅ Growth Whey (sem maltodextrina)
   - ❌ Max Titanium Whey 3W (com maltodextrina)
4. **ResponseGenerator**: Gera explicação:
   > "Recomendo Growth Whey Protein por não conter maltodextrina, 
   > o que é importante para seu controle glicêmico. O produto também 
   > oferece excelente custo-benefício com 24g de proteína por porção."
5. **AnalyticsLogger**: Salva interação

---

### Caso 2: Usuário Vegano

**Input:**
- Goal: `muscle_gain`
- Dietary Restrictions: `[vegan]`

**Fluxo:**
1. **AnamnesisCollector**: Coleta dados
2. **ScienceRetriever**: Busca dados de proteína
3. **ComparativeAnalysis**: Filtra produtos veganos
   - ✅ IntegralMedica Whey Vegan (proteína de ervilha)
   - ❌ Todos os whey de leite
4. **ResponseGenerator**: Gera explicação:
   > "Recomendo IntegralMedica Whey Vegan por ser 100% vegano, 
   > utilizando proteína de ervilha isolada. Embora tenha menos 
   > proteína por porção (22g vs 24-26g dos whey de leite), é a 
   > melhor opção para sua dieta vegana."
5. **AnalyticsLogger**: Salva interação

---

## 📊 Estrutura de Dados

### Ranking Data (JSONB)

```json
{
  "123": {
    "score": 95.5,
    "reasons": [
      "Alto teor de proteína (24g)",
      "Bom custo-benefício (R$ 3.75/g proteína)",
      "Certificações: ANVISA, GMP"
    ],
    "match_score": 0.955
  },
  "456": {
    "score": 78.3,
    "reasons": [
      "Alto teor de proteína (23g)",
      "Contém maltodextrina"
    ],
    "match_score": 0.783
  }
}
```

---

## 🔍 Boas Práticas Implementadas

### 1. Clean Code
- Código limpo e legível
- Funções pequenas e focadas
- Nomes descritivos
- Comentários onde necessário

### 2. Type Hints
- Tipagem completa em todas as funções
- `TypedDict` para estado
- Type safety garantido

### 3. Error Handling
- Tratamento adequado de erros
- Fallbacks quando possível
- Mensagens claras

### 4. Reutilização
- Funções utilitárias reutilizáveis
- Padrões consistentes
- DRY principle

### 5. Configuração Externa
- Variáveis de ambiente para LLM
- Nenhum hardcoding de credenciais
- Suporte a múltiplos ambientes (Vertex AI / Google AI Studio)

---

## 📝 Próximos Passos (Etapa 5)

Com o agente completo, a próxima etapa implementará:

1. **API REST**:
   - `POST /chat` - Endpoint principal para consultas
   - `POST /user-profile` - Criar/atualizar perfil
   - `GET /analytics/brand-performance` - Analytics de marcas

2. **Dashboard Data**:
   - Endpoints de analytics
   - Métricas de recomendação
   - Performance de produtos

---

## ✅ Checklist da Etapa 4

- [x] AgentState (TypedDict) criado
- [x] Integração Gemini 2.5 Flash (Vertex AI / Google AI Studio)
- [x] Node AnamnesisCollector implementado
- [x] Node ScienceRetriever implementado
- [x] Node ComparativeAnalysis (matchmaking) implementado
- [x] Node ResponseGenerator (com Gemini 2.5) implementado
- [x] Node AnalyticsLogger implementado
- [x] Grafo LangGraph criado e orquestrado
- [x] Runner do agente implementado
- [x] Utilitários criados
- [x] Configurações adicionadas ao config.py
- [x] Dependência langchain-google-genai adicionada
- [x] Código limpo, PEP8, type hints
- [x] Documentação completa criada
- [x] Todos os commits incrementais realizados

---

## 📚 Referências

- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Google Gemini**: https://ai.google.dev/
- **LangChain**: https://python.langchain.com/
- **Vertex AI**: https://cloud.google.com/vertex-ai
- **Google AI Studio**: https://makersuite.google.com/app/apikey

---

**Branch**: `feature/etapa-4-langgraph-agent`  
**Status**: ✅ Completa e pronta para merge

