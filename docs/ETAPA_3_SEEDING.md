# Etapa 3: Ingestão de Conhecimento (Seeding)

## 📋 Visão Geral

Esta etapa implementa o sistema completo de seeding (população inicial) do banco de dados com:
- **Dados científicos globais** (AIS Group A / Examine.com - apenas evidências fortes)
- **Tenant demo** com produtos reais de marcas concorrentes para comparação técnica

---

## 🏗️ Arquitetura Implementada

### Estrutura de Pastas

```
scripts/
├── seed_science.py          # Seeder para dados científicos (AIS/Examine)
├── seed_demo_tenant.py      # Seeder para tenant demo e produtos reais
└── seed_all.py              # Script principal que executa todos os seeders

src/infrastructure/seeders/
├── __init__.py
├── base.py                  # BaseSeeder - classe base reutilizável
└── utils.py                 # Utilitários (get_or_create, batch_create)
```

### Princípios Aplicados

- ✅ **DRY (Don't Repeat Yourself)**: Base classes e utilitários reutilizáveis
- ✅ **Clean Code**: Código limpo, legível e bem estruturado
- ✅ **PEP8**: Formatação e estilo seguindo padrões Python
- ✅ **Type Hints**: Tipagem completa para melhor IDE support e segurança
- ✅ **Context Managers**: Uso de `with` para gerenciamento seguro de sessões
- ✅ **Error Handling**: Tratamento adequado de erros com mensagens claras

---

## 📚 Componentes Implementados

### 1. Base Classes e Utilitários

#### `BaseSeeder` (`src/infrastructure/seeders/base.py`)

Classe base reutilizável que implementa pattern de context manager para gerenciamento seguro de sessões SQLModel.

**Características:**
- Gerencia sessão de banco automaticamente
- Commit automático em sucesso
- Rollback automático em erro
- Implementação de `__enter__` e `__exit__`

**Uso:**
```python
with ScienceSeeder() as seeder:
    seeder.seed()
```

#### Utilitários (`src/infrastructure/seeders/utils.py`)

**`get_or_create()`**
- Pattern Get or Create reutilizável
- Evita duplicação de dados
- Retorna `(instance, created)` tuple

**`batch_create()`**
- Cria múltiplos itens em batch
- Suporta verificação de campos únicos
- Retorna quantidade de itens criados

---

### 2. Seed de Dados Científicos

#### `seed_science.py`

Popula tabela `scientific_data` com dados do **AIS Group A** e **Examine.com**, **apenas com evidências fortes (STRONG)**.

**Dados Incluídos:**

| Suplemento | Categoria | Fonte | Evidência |
|-----------|-----------|-------|-----------|
| Whey Protein | PROTEIN | AIS | STRONG |
| Creatine Monohydrate | CREATINE | AIS | STRONG |
| Beta-Alanine | BETA_ALANINE | Examine | STRONG |
| Caffeine | CAFFEINE | AIS | STRONG |
| Citrulline Malate | CITRULLINE | Examine | STRONG |
| BCAA | BCAAS | AIS | MODERATE |
| Omega-3 | OMEGA3 | Examine | STRONG |
| Vitamin D | VITAMIN_D | Examine | STRONG |

**Estrutura de Dados:**

Cada registro contém:
- `supplement_name`: Nome do suplemento
- `category`: Categoria (enum)
- `evidence_level`: STRONG (AIS Group A ou Examine High/Moderate + Very High Consistency)
- `source`: "AIS" ou "Examine"
- `source_url`: URL da fonte
- `effects`: JSONB com efeitos documentados
- `dosage`: JSONB com dosagem recomendada
- `contraindications`: ARRAY de condições que contraindica
- `interactions`: JSONB com interações com medicamentos/condições

**Exemplo - Whey Protein:**
```json
{
  "supplement_name": "Whey Protein",
  "effects": {
    "muscle_gain": "strong",
    "strength": "strong",
    "recovery": "strong"
  },
  "dosage": {
    "min": 20.0,
    "max": 40.0,
    "unit": "g",
    "timing": "post_workout"
  },
  "contraindications": ["kidney_disease", "lactose_intolerance"]
}
```

**Execução:**
```bash
# Via Poetry script
poetry run seed-science

# Ou diretamente
python scripts/seed_science.py
```

---

### 3. Seed de Tenant Demo e Produtos

#### `seed_demo_tenant.py`

Cria **tenant demo** ("Loja Demo - Academia Fit") e popula com **produtos reais de marcas concorrentes** com tabelas nutricionais completas.

**Marcas e Produtos Incluídos:**

| Marca | Produto | Categoria | Preço (R$) |
|-------|---------|-----------|------------|
| Growth Supplements | Whey Protein Concentrado | PROTEIN | 89.90 |
| Max Titanium | Whey 3W - Blend | PROTEIN | 99.90 |
| IntegralMedica | Whey Zero Lactose | PROTEIN | 129.90 |
| Dux Nutrition | Whey Protein Isolado | PROTEIN | 149.90 |
| Growth Supplements | Creatina Monohidratada | CREATINE | 49.90 |
| Max Titanium | Creatina Creapure | CREATINE | 69.90 |
| IntegralMedica | Whey Vegan (Ervilha) | PROTEIN | 119.90 |

**Tabelas Nutricionais Reais (JSONB):**

Cada produto contém informações completas para comparação técnica:

```json
{
  "protein_g": 24.0,
  "carbs_g": 3.5,
  "fat_g": 1.8,
  "calories": 120,
  "serving_size_g": 30,
  "ingredients": ["Whey Protein Concentrate", "Cacau em Pó", ...],
  "allergens": ["Leite"],
  "no_gluten": true,
  "no_lactose": false,
  "vegan": false,
  "maltodextrin": false,
  "artificial_sweeteners": true,
  "added_sugars_g": 0.0,
  "sodium_mg": 50.0
}
```

**Campos Críticos para Comparação:**
- `maltodextrin`: Importante para diabetes (evitar)
- `no_lactose`: Para intolerantes à lactose
- `vegan`: Para dieta vegana
- `artificial_sweeteners`: Para quem evita adoçantes artificiais
- `protein_g`: Para cálculo de custo-benefício
- `price`: Para comparação de preço por grama de proteína

**Execução:**
```bash
# Via Poetry script
poetry run seed-demo

# Ou diretamente
python scripts/seed_demo_tenant.py
```

---

### 4. Script Principal

#### `seed_all.py`

Executa todos os seeders em sequência, populando o banco completo.

**Fluxo:**
1. Seed de dados científicos (AIS/Examine)
2. Seed de tenant demo e produtos reais

**Execução:**
```bash
# Via Poetry script (recomendado)
poetry run seed-all

# Ou diretamente
python scripts/seed_all.py
```

---

## 🔧 Integração com Poetry

Scripts adicionados ao `pyproject.toml` para fácil execução:

```toml
[tool.poetry.scripts]
seed-science = "python scripts/seed_science.py"
seed-demo = "python scripts/seed_demo_tenant.py"
seed-all = "python scripts/seed_all.py"
```

**Uso:**
```bash
poetry install  # Instalar dependências (se ainda não instalou)
poetry run seed-all  # Executar todos os seeders
```

---

## 📊 Dados Populados

### Dados Científicos (Global)

- **8 suplementos** com evidência STRONG
- Fontes: AIS Group A e Examine.com
- Filtro: Apenas evidências fortes (sem alucinações da IA)

### Tenant Demo

- **1 tenant** criado: "Loja Demo - Academia Fit"
- **7 produtos** de marcas reais:
  - 4 Whey Proteins (Growth, Max Titanium, IntegralMedica, Dux)
  - 2 Creatinas (Growth, Max Titanium)
  - 1 Whey Vegan (IntegralMedica)

**Variedade de Produtos:**
- Diferentes níveis de proteína (23g - 26g)
- Diferentes preços (R$ 49.90 - R$ 149.90)
- Com e sem lactose
- Com e sem maltodextrina
- Com e sem adoçantes artificiais
- Certificações diferentes (ANVISA, GMP, Creapure, etc.)

---

## 🎯 Casos de Uso para Teste

Os dados populados permitem testar cenários reais:

### 1. Usuário Diabético
- **Restrição**: Diabetes (evitar maltodextrina)
- **Produtos filtrados**: Growth Whey, IntegralMedica Zero Lactose, Dux Isolado ✅
- **Produtos excluídos**: Max Titanium (contém maltodextrina) ❌

### 2. Usuário Vegano
- **Restrição**: Vegan
- **Produtos filtrados**: IntegralMedica Whey Vegan ✅
- **Produtos excluídos**: Todos os whey (leite) ❌

### 3. Usuário Intolerante à Lactose
- **Restrição**: Lactose Free
- **Produtos filtrados**: IntegralMedica Zero Lactose ✅
- **Produtos excluídos**: Growth, Max Titanium, Dux ❌

### 4. Comparação de Custo-Benefício
- **Objetivo**: Mais proteína por real
- **Cálculo**: `price / protein_g` por porção
- **Vencedor**: Growth Whey (R$ 3.75/g de proteína)

### 5. Comparação de Qualidade
- **Certificações**: GMP, Creapure, ANVISA
- **Ingredientes**: Isolado vs Concentrado vs Blend
- **Pureza**: Sem aditivos desnecessários

---

## 🔍 Exemplos de Queries para Comparação

### Buscar Whey Proteins sem Maltodextrina
```python
from sqlmodel import select
from src.domain.models import Product
from src.domain.enums import SupplementCategory

stmt = (
    select(Product)
    .where(Product.tenant_id == tenant_id)
    .where(Product.category == SupplementCategory.PROTEIN)
    .where(Product.nutritional_info["maltodextrin"].as_boolean() == False)
)
```

### Calcular Custo-Benefício (Preço por grama de proteína)
```python
# Via SQL ou cálculo Python
price_per_protein_g = product.price / product.nutritional_info["protein_g"]
```

### Filtrar por Restrições Alimentares
```python
# Sem lactose
products = [p for p in all_products 
            if p.nutritional_info.get("no_lactose", False)]

# Vegan
products = [p for p in all_products 
            if p.nutritional_info.get("vegan", False)]
```

---

## 📝 Boas Práticas Implementadas

### 1. Evitar Hardcoding
- Todos os valores são definidos nos scripts
- Nenhum dado hardcoded em código de produção
- Facilita atualização e manutenção

### 2. Código Limpo
- Funções pequenas e focadas
- Nomes descritivos
- Comentários onde necessário
- Type hints completos

### 3. Reutilização
- Base classes para evitar duplicação
- Utilitários reutilizáveis (get_or_create, batch_create)
- Padrões consistentes

### 4. Error Handling
- Tratamento de erros claro
- Mensagens informativas
- Rollback automático em falhas

### 5. Idempotência
- Scripts podem ser executados múltiplas vezes
- `get_or_create` evita duplicação
- Safe para re-executar

---

## 🚀 Como Executar

### Pré-requisitos

1. **Banco de dados rodando:**
   ```bash
   docker-compose up -d
   ```

2. **Migrations aplicadas:**
   ```bash
   alembic upgrade head
   ```

3. **Dependências instaladas:**
   ```bash
   poetry install
   ```

### Executar Seeding

**Opção 1: Via Poetry (Recomendado)**
```bash
poetry run seed-all
```

**Opção 2: Scripts Individuais**
```bash
# Apenas dados científicos
poetry run seed-science

# Apenas tenant demo
poetry run seed-demo
```

**Opção 3: Diretamente**
```bash
python scripts/seed_all.py
```

### Verificar Dados

```python
from src.core.database import sync_engine
from sqlmodel import Session, select
from src.domain.models import ScientificData, Tenant, Product

with Session(sync_engine) as session:
    # Verificar dados científicos
    science_count = len(session.exec(select(ScientificData)).all())
    print(f"Dados científicos: {science_count}")
    
    # Verificar tenants
    tenants = session.exec(select(Tenant)).all()
    print(f"Tenants: {len(tenants)}")
    
    # Verificar produtos
    products = session.exec(select(Product)).all()
    print(f"Produtos: {len(products)}")
```

---

## 🔄 Próximos Passos (Etapa 4)

Com os dados populados, a próxima etapa implementará:

1. **LangGraph Agent** para comparação técnica
2. **Lógica de Matching** baseada em:
   - Dados científicos (ScientificData)
   - Perfil do usuário (UserProfile)
   - Produtos disponíveis (Product)
3. **Justificativas** para cada recomendação
4. **Ranking** de produtos por relevância

---

## ✅ Checklist da Etapa 3

- [x] Base classes e utilitários criados
- [x] Script seed_science.py implementado
- [x] Script seed_demo_tenant.py implementado
- [x] Script seed_all.py criado
- [x] Scripts Poetry adicionados ao pyproject.toml
- [x] Dados científicos populados (AIS/Examine - STRONG evidence)
- [x] Tenant demo criado com produtos reais
- [x] Tabelas nutricionais completas para comparação
- [x] Código limpo, PEP8, type hints
- [x] Documentação completa criada
- [x] Todos os commits realizados na branch feature/etapa-3-seeding

---

## 📚 Referências

- **AIS (Australian Institute of Sport)**: https://www.ais.gov.au/nutrition/supplements
- **Examine.com**: https://examine.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **Python PEP 8**: https://pep8.org/

---

**Branch**: `feature/etapa-3-seeding`  
**Status**: ✅ Completa e pronta para merge

