# 🐳 Docker Guide - SmartSupp

Guia completo para usar Docker e Docker Compose com SmartSupp.

---

## 🚀 Iniciando os Serviços

### Build e Start

```bash
# Build das imagens e iniciar serviços
docker compose up -d --build

# Apenas iniciar (se já tiver buildado)
docker compose up -d
```

**O que isso faz:**
- ✅ Constrói a imagem da aplicação (se necessário)
- ✅ Inicia PostgreSQL na porta 5435
- ✅ Inicia API na porta 8003
- ✅ Configura rede interna entre serviços

---

## 📝 Ver Logs

### Logs de todos os serviços

```bash
# Ver logs de todos os serviços em tempo real
docker compose logs -f

# Ver últimas 100 linhas
docker compose logs --tail=100

# Ver logs desde um tempo específico
docker compose logs --since 10m
```

### Logs apenas da API

```bash
# Ver logs da API em tempo real
docker compose logs -f app

# Últimas 50 linhas da API
docker compose logs --tail=50 app

# Ver logs da API desde início
docker compose logs app
```

### Logs apenas do PostgreSQL

```bash
# Ver logs do PostgreSQL
docker compose logs -f postgres

# Últimas 100 linhas do PostgreSQL
docker compose logs --tail=100 postgres
```

### Logs de múltiplos serviços

```bash
# Ver logs de serviços específicos
docker compose logs -f app postgres
```

---

## 🔍 Comandos Úteis

### Status dos Serviços

```bash
# Ver status de todos os serviços
docker compose ps

# Ver status detalhado
docker compose ps -a
```

### Parar Serviços

```bash
# Parar todos os serviços (mantém containers)
docker compose stop

# Parar e remover containers
docker compose down

# Parar, remover containers e volumes
docker compose down -v
```

### Reiniciar Serviços

```bash
# Reiniciar todos os serviços
docker compose restart

# Reiniciar apenas a API
docker compose restart app

# Reiniciar apenas o PostgreSQL
docker compose restart postgres
```

### Rebuild

```bash
# Rebuild da aplicação
docker compose build app

# Rebuild forçado (sem cache)
docker compose build --no-cache app

# Rebuild e reiniciar
docker compose up -d --build app
```

---

## 🛠️ Executar Comandos Dentro dos Containers

### Dentro do container da API

```bash
# Shell interativo
docker compose exec app bash

# Executar comando específico
docker compose exec app poetry run alembic upgrade head
docker compose exec app poetry run python scripts/seed_all.py

# Executar Python
docker compose exec app python -c "from src.core.config import settings; print(settings.APP_NAME)"
```

### Dentro do container do PostgreSQL

```bash
# Acessar PostgreSQL CLI
docker compose exec postgres psql -U smartsupp -d smartsupp

# Executar SQL
docker compose exec postgres psql -U smartsupp -d smartsupp -c "SELECT COUNT(*) FROM tenants;"
```

---

## 🔧 Desenvolvimento

### Hot Reload

O Docker Compose já está configurado para hot reload:
- O código em `./src` é montado como volume
- Mudanças em arquivos Python recarregam automaticamente
- Logs mostram quando recarrega

### Ver logs durante desenvolvimento

```bash
# Terminal 1: Iniciar serviços
docker compose up -d --build

# Terminal 2: Acompanhar logs
docker compose logs -f app
```

---

## 🐛 Troubleshooting

### Ver logs de erros

```bash
# Logs apenas de erro
docker compose logs app | grep -i error

# Logs de erro em tempo real
docker compose logs -f app | grep -i error
```

### Verificar saúde dos serviços

```bash
# Status dos health checks
docker compose ps

# Verificar health check da API manualmente
docker compose exec app curl -f http://localhost:8003/health
```

### Limpar tudo e recomeçar

```bash
# Parar tudo
docker compose down -v

# Remover imagens
docker compose down --rmi all

# Rebuild completo
docker compose build --no-cache
docker compose up -d
```

### Ver uso de recursos

```bash
# Stats em tempo real
docker stats smartsupp_app smartsupp_db

# Ver uso de disco
docker system df
```

---

## 📊 Exemplo de Uso Completo

```bash
# 1. Build e iniciar
docker compose up -d --build

# 2. Ver logs
docker compose logs -f app

# 3. Executar migrations
docker compose exec app poetry run alembic upgrade head

# 4. Popular dados
docker compose exec app poetry run python scripts/seed_all.py

# 5. Testar API
curl http://localhost:8003/health

# 6. Ver logs do PostgreSQL
docker compose logs -f postgres

# 7. Parar tudo
docker compose down
```

---

## 🔐 Variáveis de Ambiente

As variáveis são carregadas do arquivo `.env`:

```env
# Database
POSTGRES_USER=smartsupp
POSTGRES_PASSWORD=smartsupp_dev
POSTGRES_DB=smartsupp
POSTGRES_PORT=5435

# App
APP_PORT=8003
DEBUG=True
SECRET_KEY=sua-chave-secreta

# LLM
GOOGLE_API_KEY=sua-api-key
```

**Importante:** O `.env` não deve ser commitado no Git!

---

## 📱 Acessar Serviços

Após iniciar com `docker compose up -d`:

- **API**: http://localhost:8003
- **Swagger UI**: http://localhost:8003/docs
- **ReDoc**: http://localhost:8003/redoc
- **Health Check**: http://localhost:8003/health
- **PostgreSQL**: localhost:5435

---

## ✅ Resumo dos Comandos

**Iniciar:**
```bash
docker compose up -d --build
```

**Ver logs:**
```bash
docker compose logs -f
docker compose logs -f app
docker compose logs -f postgres
```

**Parar:**
```bash
docker compose down
```

**Rebuild:**
```bash
docker compose build --no-cache app
docker compose up -d
```

---

**Pronto! Agora você pode usar Docker Compose corretamente! 🎉**

