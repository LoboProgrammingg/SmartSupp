-- PostgreSQL initialization script
-- Executado automaticamente na primeira inicialização do container

-- Criar extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- Para busca fuzzy (busca de produtos)

-- Comentário
COMMENT ON DATABASE smartsupp IS 'SmartSupp - SaaS Multitenant de Recomendação de Suplementos Esportivos';

