# Schema do Banco de Dados - SmartSupp

## 📊 Visão Geral

Este documento descreve a modelagem de dados do SmartSupp, focada em **comparação técnica de produtos** entre marcas concorrentes.

---

## 🏗️ Estratégia Multitenant

- **Isolamento**: Todas as tabelas de negócio possuem `tenant_id`
- **Global**: `ScientificData` é **sem tenant_id** - compartilhada por todos
- **Segurança**: Middleware e Dependencies garantem isolamento automático

---

## 📋 Tabelas

### 1. `tenants`
Cliente/Loja que usa a plataforma.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER PK | ID único do tenant |
| `name` | VARCHAR(255) | Nome do tenant |
| `plan` | ENUM | Plano (FREE, BASIC, PRO, ENTERPRISE) |
| `created_at` | TIMESTAMP | Data de criação |
| `updated_at` | TIMESTAMP | Data de atualização |

**Índices**: `name`

---

### 2. `scientific_data` ⚛️ GLOBAL
Dados científicos globais (AIS/Examine) - **SEM tenant_id**.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER PK | ID único |
| `supplement_name` | VARCHAR(255) | Nome do suplemento |
| `category` | ENUM | Categoria (PROTEIN, CREATINE, etc.) |
| `evidence_level` | ENUM | Nível de evidência (STRONG, MODERATE, WEAK) |
| `source` | VARCHAR(100) | Fonte ("AIS" ou "Examine") |
| `source_url` | VARCHAR(500) | URL da fonte |
| `effects` | JSONB | Efeitos documentados |
| `dosage` | JSONB | Dosagem recomendada |
| `contraindications` | ARRAY[String] | Condições que contraindica |
| `interactions` | JSONB | Interações com medicamentos |
| `created_at` | TIMESTAMP | Data de criação |
| `updated_at` | TIMESTAMP | Data de atualização |

**Índices**: `supplement_name`, `category`, `evidence_level`, `source`

**Estrutura JSONB `effects`**:
```json
{
  "muscle_gain": "strong",
  "strength": "moderate",
  "recovery": "strong"
}
```

**Estrutura JSONB `dosage`**:
```json
{
  "min": 5.0,
  "max": 10.0,
  "unit": "g",
  "timing": "post_workout"
}
```

---

### 3. `user_profiles` 👤 (Por Tenant)
Perfil do usuário - dados de anamnese.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER PK | ID único |
| `tenant_id` | INTEGER FK | Referência ao tenant |
| `biometrics` | JSONB | Dados vitais (peso, altura, idade, sexo, BMI) |
| `goal` | ENUM | Objetivo (WEIGHT_LOSS, MUSCLE_GAIN, etc.) |
| `dietary_restrictions` | ARRAY[String] | Restrições alimentares |
| `medical_conditions` | ARRAY[String] | Condições médicas |
| `budget_range` | ENUM | Faixa de orçamento (LOW, MEDIUM, HIGH, PREMIUM) |
| `created_at` | TIMESTAMP | Data de criação |
| `updated_at` | TIMESTAMP | Data de atualização |

**Índices**: `tenant_id`, `goal`, `budget_range`, `(tenant_id, goal)`

**Estrutura JSONB `biometrics`**:
```json
{
  "weight_kg": 75.5,
  "height_cm": 175,
  "age": 30,
  "sex": "male",
  "bmi": 24.7
}
```

---

### 4. `products` 📦 (Por Tenant)
Produto/Suplemento disponível no estoque do tenant.

**Foco**: Comparação técnica entre marcas concorrentes.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER PK | ID único |
| `tenant_id` | INTEGER FK | Referência ao tenant |
| `brand_name` | VARCHAR(255) | Nome da marca |
| `product_name` | VARCHAR(255) | Nome do produto |
| `category` | ENUM | Categoria do suplemento |
| `nutritional_info` | JSONB | **Tabela nutricional completa** |
| `certifications` | ARRAY[String] | Certificações (ANVISA, GMP, VEGAN, etc.) |
| `price` | FLOAT | Preço em R$ |
| `currency` | VARCHAR(3) | Moeda (BRL) |
| `stock_quantity` | INTEGER | Quantidade em estoque |
| `is_active` | BOOLEAN | Produto ativo |
| `created_at` | TIMESTAMP | Data de criação |
| `updated_at` | TIMESTAMP | Data de atualização |

**Índices**: `tenant_id`, `brand_name`, `category`, `(tenant_id, category)`, `(is_active, tenant_id)`, `price`

**Estrutura JSONB `nutritional_info`** (Crítico para comparação):
```json
{
  "protein_g": 25.0,
  "carbs_g": 3.0,
  "fat_g": 1.5,
  "calories": 120,
  "serving_size_g": 30,
  "ingredients": [
    "Whey Protein Concentrate",
    "Cocoa Powder",
    "Stevia"
  ],
  "allergens": ["Milk"],
  "no_gluten": true,
  "no_lactose": false,
  "vegan": false,
  "maltodextrin": false,
  "artificial_sweeteners": false,
  "added_sugars_g": 0.0
}
```

**Uso na Comparação**:
- Verificar `allergens` vs `medical_conditions`
- Verificar `no_gluten`, `no_lactose`, `vegan` vs `dietary_restrictions`
- Verificar `maltodextrin` vs diabetes
- Comparar `protein_g` por grama de produto
- Comparar `price` por grama de proteína

---

### 5. `interaction_logs` 📊 (Por Tenant)
Log de interações para BI e Analytics.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER PK | ID único |
| `tenant_id` | INTEGER FK | Referência ao tenant |
| `user_profile_id` | INTEGER FK | Referência ao perfil |
| `session_id` | VARCHAR(255) | ID da sessão |
| `query_text` | TEXT | Texto da consulta |
| `recommended_products` | ARRAY[String] | IDs dos produtos recomendados |
| `ranking_data` | JSONB | Dados de ranking e justificativas |
| `selected_product_id` | INTEGER FK | ID do produto selecionado |
| `user_feedback` | TEXT | Feedback do usuário |
| `satisfaction_score` | INTEGER | Score de 1-5 |
| `created_at` | TIMESTAMP | Data da interação |
| `ip_address` | VARCHAR(45) | IP do usuário |
| `user_agent` | VARCHAR(500) | User agent do navegador |

**Índices**: `tenant_id`, `created_at`, `(tenant_id, created_at)`, `selected_product_id`, `session_id`

**Estrutura JSONB `ranking_data`**:
```json
{
  "product_123": {
    "score": 95.5,
    "reasons": [
      "Não contém maltodextrina (importante para diabetes)",
      "Melhor custo-benefício por grama de proteína",
      "Certificação ANVISA e GMP"
    ],
    "match_score": 0.92
  },
  "product_456": {
    "score": 78.3,
    "reasons": [
      "Contém lactose (restrição alimentar)",
      "Preço mais alto"
    ],
    "match_score": 0.65
  }
}
```

---

## 🔍 Queries Principais

### Buscar produtos por categoria e tenant
```sql
SELECT * FROM products
WHERE tenant_id = :tenant_id
  AND category = :category
  AND is_active = true
ORDER BY price;
```

### Comparar produtos (com filtros de restrições)
```sql
SELECT 
  p.*,
  p.nutritional_info->>'protein_g' as protein_g,
  p.nutritional_info->>'maltodextrin' as maltodextrin,
  p.price / CAST(p.nutritional_info->>'protein_g' AS FLOAT) as price_per_protein_g
FROM products p
WHERE p.tenant_id = :tenant_id
  AND p.category = :category
  AND p.is_active = true
  AND (
    -- Filtro: sem maltodextrina (para diabetes)
    (p.nutritional_info->>'maltodextrin')::boolean = false
    OR (p.nutritional_info->>'maltodextrin') IS NULL
  )
ORDER BY price_per_protein_g ASC;
```

### Buscar dados científicos
```sql
SELECT * FROM scientific_data
WHERE supplement_name ILIKE :search
  AND evidence_level = 'strong'
ORDER BY source;
```

### Analytics: Produtos mais recomendados
```sql
SELECT 
  p.brand_name,
  p.product_name,
  COUNT(il.id) as recommendation_count,
  AVG(il.satisfaction_score) as avg_satisfaction
FROM interaction_logs il
JOIN products p ON p.id = ANY(
  SELECT CAST(unnest AS INTEGER) 
  FROM unnest(il.recommended_products)
)
WHERE il.tenant_id = :tenant_id
  AND il.created_at >= NOW() - INTERVAL '30 days'
GROUP BY p.id, p.brand_name, p.product_name
ORDER BY recommendation_count DESC;
```

---

## 📝 Notas Importantes

1. **Multitenancy**: Sempre filtrar por `tenant_id` (exceto `ScientificData`)
2. **JSONB**: Use operadores JSONB do PostgreSQL para queries eficientes
3. **Índices**: Criados para queries frequentes (busca, comparação, analytics)
4. **Foreign Keys**: Garantem integridade referencial
5. **Timestamps**: `created_at` e `updated_at` para auditoria

---

## 🚀 Próximos Passos

- **Etapa 3**: Seeding de dados científicos (AIS/Examine) e produtos demo
- **Etapa 4**: Implementar agente LangGraph para comparação técnica
- **Etapa 5**: API REST e endpoints de analytics

