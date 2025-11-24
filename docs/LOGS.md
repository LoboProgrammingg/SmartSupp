# 📝 Guia de Logs - SmartSupp

Como acompanhar e gerenciar logs da aplicação SmartSupp.

---

## 🚀 Opções para Acompanhar Logs

### 1️⃣ **Foreground (Ver logs direto no terminal)**

Melhor para desenvolvimento - você vê tudo em tempo real:

```bash
poetry run dev
```

**Vantagens:**
- ✅ Logs em tempo real no terminal
- ✅ Cores e formatação preservadas
- ✅ Fácil de parar (Ctrl+C)

**Quando usar:**
- Desenvolvimento ativo
- Debugging
- Testes locais

---

### 2️⃣ **Background com logs em arquivo**

Útil quando você quer rodar a API e continuar usando o terminal:

```bash
# Iniciar em background
poetry run dev-bg

# Acompanhar logs em tempo real
tail -f logs/api.log

# Ver últimas 50 linhas
tail -n 50 logs/api.log

# Buscar erros
grep -i error logs/api.log

# Ver logs e filtrar
tail -f logs/api.log | grep -i "error\|warning"
```

**Arquivo de log:**
- `logs/api.log` - Todos os logs da API

**Vantagens:**
- ✅ API roda em background
- ✅ Logs salvos para consulta posterior
- ✅ Pode continuar usando o terminal

---

### 3️⃣ **Usando `tail` em tempo real**

Após iniciar em background, acompanhe logs:

```bash
# Ver logs em tempo real (follow)
tail -f logs/api.log

# Com cores (se tiver bat/ccat instalado)
tail -f logs/api.log | bat --paging=never
# ou
tail -f logs/api.log | ccat -C
```

**Atalhos úteis:**
- `Ctrl+C` - Parar de acompanhar
- `Ctrl+F` - Seguir arquivo (se foi truncado)

---

### 4️⃣ **Ver últimos logs**

```bash
# Últimas 100 linhas
tail -n 100 logs/api.log

# Últimas 50 linhas + seguir
tail -n 50 -f logs/api.log

# Primeiras 100 linhas (início da execução)
head -n 100 logs/api.log
```

---

### 5️⃣ **Buscar e filtrar logs**

```bash
# Buscar erros
grep -i error logs/api.log

# Buscar requisições específicas
grep "POST /chat" logs/api.log

# Buscar com contexto (3 linhas antes/depois)
grep -i -C 3 error logs/api.log

# Buscar e mostrar apenas horário e mensagem
grep -i error logs/api.log | awk '{print $1, $2, $NF}'

# Buscar hoje
grep "$(date +%Y-%m-%d)" logs/api.log

# Contar ocorrências
grep -i error logs/api.log | wc -l
```

---

### 6️⃣ **Rotação de logs**

Para evitar arquivos de log muito grandes:

```bash
# Rotacionar manualmente
mv logs/api.log logs/api.log.$(date +%Y%m%d_%H%M%S)
touch logs/api.log

# Usar logrotate (Linux)
# Criar /etc/logrotate.d/smartsupp:
# /caminho/para/smartsupp/logs/*.log {
#     daily
#     rotate 7
#     compress
#     delaycompress
#     missingok
#     notifempty
# }
```

---

### 7️⃣ **Usando `screen` ou `tmux`**

Mantém a sessão mesmo fechando o terminal:

#### **Screen:**

```bash
# Criar sessão
screen -S smartsupp

# Dentro do screen, iniciar API
poetry run dev

# Desanexar: Ctrl+A, depois D

# Reanexar depois
screen -r smartsupp

# Listar sessões
screen -ls
```

#### **Tmux:**

```bash
# Criar sessão
tmux new -s smartsupp

# Dentro do tmux, iniciar API
poetry run dev

# Desanexar: Ctrl+B, depois D

# Reanexar depois
tmux attach -t smartsupp

# Listar sessões
tmux ls
```

---

## 🛠️ Níveis de Log

O Uvicorn suporta diferentes níveis de log. Para alterar, edite `scripts/dev.py`:

```python
cmd = [
    "uvicorn",
    "src.main:app",
    "--log-level", "debug",  # debug, info, warning, error, critical
    ...
]
```

**Níveis disponíveis:**
- `debug` - Muito detalhado (mais verbose)
- `info` - Informações gerais (padrão)
- `warning` - Avisos
- `error` - Apenas erros
- `critical` - Apenas críticos

---

## 📊 Exemplo de Logs

### Logs normais:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
INFO:     127.0.0.1:54321 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:54321 - "POST /chat HTTP/1.1" 200 OK
```

### Logs de erro:

```
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "...", line X, in ...
    ...
SomeError: mensagem de erro
```

---

## 🔍 Comandos Úteis

### Ver processos relacionados:

```bash
# Ver se a API está rodando
ps aux | grep "uvicorn.*8003"

# Ver PID do processo
pgrep -f "uvicorn.*8003"

# Matar processo
pkill -f "uvicorn.*8003"
# ou
kill $(pgrep -f "uvicorn.*8003")
```

### Ver porta em uso:

```bash
# Ver quem está usando porta 8003
lsof -i :8003
# ou
netstat -tulpn | grep 8003
```

### Limpar logs antigos:

```bash
# Apagar logs antigos
rm logs/api.log.*

# Limpar arquivo atual (sem parar API)
> logs/api.log

# Manter apenas últimos 1000 linhas
tail -n 1000 logs/api.log > logs/api.log.tmp
mv logs/api.log.tmp logs/api.log
```

---

## 📱 Integração com Monitoramento

### Usando `multitail` (instalar primeiro):

```bash
# Ubuntu/Debian
sudo apt install multitail

# Ver múltiplos logs
multitail logs/api.log logs/access.log
```

### Usando `less` para navegação:

```bash
# Abrir logs
less logs/api.log

# Navegação:
# - Espaço: próxima página
# - b: página anterior
# - /termo: buscar
# - n: próximo resultado
# - N: anterior
# - q: sair
```

---

## ✅ Resumo Rápido

**Desenvolvimento:**
```bash
poetry run dev  # Ver logs no terminal
```

**Produção/Background:**
```bash
poetry run dev-bg              # Iniciar em background
tail -f logs/api.log          # Acompanhar logs
```

**Debug:**
```bash
tail -f logs/api.log | grep -i error
```

**Parar API:**
```bash
pkill -f "uvicorn.*8003"
```

---

**Pronto! Agora você sabe como acompanhar todos os logs da aplicação! 🎉**

