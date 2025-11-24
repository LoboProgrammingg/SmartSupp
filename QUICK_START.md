# 🚀 Quick Start - SmartSupp Localhost

Guia rápido para rodar o SmartSupp em localhost.

## 📋 Pré-requisitos

1. **Python 3.11+**
2. **Poetry** ([Instalar](https://python-poetry.org/docs/#installation))
3. **Docker e Docker Compose** ([Instalar](https://docs.docker.com/get-docker/))
4. **PostgreSQL** (via Docker Compose ou local)
5. **Google API Key** (para Gemini) - [Obter aqui](https://makersuite.google.com/app/apikey)

---

## 🔧 Passo a Passo

### 1. Clonar e Configurar

```bash
# Clonar repositório (se ainda não clonou)
git clone https://github.com/LoboProgrammingg/SmartSupp.git
cd smartsupp

# Copiar .env.example para .env
cp .env.example .env

# Editar .env com suas configurações
nano .env  # ou use seu editor preferido
```

### 2. Configurar .env

**Mínimo necessário para funcionar:**

```env
# Database (valores padrão do docker-compose)
POSTGRES_USER=smartsupp
POSTGRES_PASSWORD=smartsupp_dev
POSTGRES_DB=smartsupp
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Security (gere uma chave segura!)
SECRET_KEY=sua-chave-secreta-aqui
# Gere com: python -c "import secrets; print(secrets.token_urlsafe(32))"

# LLM (Google AI Studio - mais fácil para desenvolvimento)
GOOGLE_API_KEY=sua-api-key-do-google-aqui
GEMINI_MODEL=gemini-2.0-flash-exp

# App
DEBUG=True
```

**Gerar SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
# ou
openssl rand -hex 32
```

**Obter Google API Key:**
1. Acesse: https://makersuite.google.com/app/apikey
2. Crie uma nova API Key
3. Cole no `.env` como `GOOGLE_API_KEY`

---

### 3. Iniciar PostgreSQL

```bash
# Subir PostgreSQL via Docker Compose
docker-compose up -d

# Verificar se está rodando
docker-compose ps

# Ver logs (opcional)
docker-compose logs -f postgres
```

**Se preferir PostgreSQL local:**
- Instale PostgreSQL
- Crie banco: `createdb smartsupp`
- Atualize `.env` com suas credenciais

---

### 4. Instalar Dependências

```bash
# Instalar Poetry (se ainda não instalou)
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependências do projeto
poetry install

# Ativar ambiente virtual
poetry shell
```

---

### 5. Executar Migrations

```bash
# Aplicar migrations do Alembic
alembic upgrade head

# Verificar status
alembic current
```

---

### 6. Popular Banco de Dados (Seeding)

```bash
# Popular dados científicos e tenant demo
poetry run seed-all

# Ou individualmente:
poetry run seed-science      # Apenas dados científicos
poetry run seed-demo         # Apenas tenant demo
```

---

### 7. Iniciar Aplicação

```bash
# Via Poetry (recomendado)
poetry run dev

# Ou diretamente com uvicorn
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: **http://localhost:8000**

---

### 8. Testar a API

#### Acessar Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### Criar Perfil de Usuário

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

---

## ✅ Verificar se Está Funcionando

### Health Check

```bash
curl http://localhost:8000/health
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Testar Endpoints no Swagger

1. Acesse: http://localhost:8000/docs
2. Expanda `POST /chat`
3. Clique em "Try it out"
4. Preencha o JSON com:
   ```json
   {
     "user_input": "Qual whey protein é melhor?",
     "user_profile_id": 1
   }
   ```
5. Clique em "Execute"
6. Verifique a resposta

---

## 🐛 Troubleshooting

### Erro: "Configuração LLM inválida"

**Solução:**
- Verifique se `GOOGLE_API_KEY` está configurado no `.env`
- Verifique se a API Key é válida
- Tente obter uma nova API Key em https://makersuite.google.com/app/apikey

### Erro: "Could not connect to database"

**Solução:**
```bash
# Verificar se PostgreSQL está rodando
docker-compose ps

# Se não estiver, iniciar
docker-compose up -d

# Verificar logs
docker-compose logs postgres

# Testar conexão
psql -h localhost -U smartsupp -d smartsupp
```

### Erro: "No such table"

**Solução:**
```bash
# Aplicar migrations
alembic upgrade head

# Verificar se migrations foram aplicadas
alembic current
```

### Erro: "Module not found"

**Solução:**
```bash
# Reinstalar dependências
poetry install

# Verificar ambiente virtual
poetry shell
which python
```

---

## 📚 Próximos Passos

1. **Executar Testes:**
   ```bash
   poetry run pytest
   ```

2. **Ver Coverage:**
   ```bash
   poetry run pytest --cov=src --cov-report=html
   open htmlcov/index.html
   ```

3. **Explorar API:**
   - Acesse http://localhost:8000/docs
   - Teste todos os endpoints
   - Veja os dados de exemplo

4. **Ler Documentação:**
   - `/docs/ETAPA_1.md` - Infraestrutura
   - `/docs/ETAPA_2.md` - Modelagem
   - `/docs/ETAPA_3.md` - Seeding
   - `/docs/ETAPA_4.md` - LangGraph
   - `/docs/ETAPA_5.md` - API
   - `/docs/TESTES.md` - Testes

---

## 🔐 Segurança

⚠️ **IMPORTANTE para Produção:**

1. **Gere SECRET_KEY única e segura**
2. **Nunca commite o arquivo .env**
3. **Use variáveis de ambiente do sistema em produção**
4. **Configure CORS adequadamente**
5. **Use JWT ao invés de header X-Tenant-ID**

---

## 📞 Suporte

- **Repositório**: https://github.com/LoboProgrammingg/SmartSupp
- **Issues**: https://github.com/LoboProgrammingg/SmartSupp/issues
- **Documentação**: Ver pasta `/docs`

---

**Pronto! A API está rodando em localhost! 🎉**

