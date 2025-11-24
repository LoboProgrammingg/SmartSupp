FROM python:3.12-slim

WORKDIR /app

# Instalar Poetry
RUN pip install poetry==2.1.3 && \
    poetry config virtualenvs.create false

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Instalar dependências
RUN poetry install --no-interaction --no-ansi --no-root

# Copiar código da aplicação
COPY . .

# Instalar a aplicação
RUN poetry install --no-interaction --no-ansi

# Variáveis de ambiente padrão
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expor porta
EXPOSE 8003

# Comando para iniciar a aplicação
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8003", "--reload", "--log-level", "info"]

