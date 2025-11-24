"""
Database Configuration and SQLModel Setup
Estratégia Multitenant: Isolamento via tenant_id em todas as tabelas de negócio
"""
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from src.core.config import settings

# Engine síncrono para migrations (Alembic)
sync_engine = create_engine(
    settings.DATABASE_URL_SYNC,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# Engine assíncrono para operações da aplicação
async_engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=settings.DEBUG,
    poolclass=NullPool if settings.TESTING else None,
    pool_pre_ping=True,
    future=True,
)

# Session factory assíncrona
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def init_db() -> None:
    """Inicializa o banco de dados criando todas as tabelas"""
    SQLModel.metadata.create_all(sync_engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency para FastAPI que retorna uma sessão de banco assíncrona
    Com isolamento automático de tenant via middleware
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


class TenantScope:
    """
    Context Manager para escopo de tenant
    Garante que todas as queries sejam filtradas pelo tenant_id ativo
    """
    _current_tenant_id: int | None = None

    @classmethod
    def set_tenant(cls, tenant_id: int) -> None:
        """Define o tenant ativo no contexto da requisição"""
        cls._current_tenant_id = tenant_id

    @classmethod
    def get_tenant(cls) -> int | None:
        """Retorna o tenant_id ativo"""
        return cls._current_tenant_id

    @classmethod
    def clear_tenant(cls) -> None:
        """Limpa o tenant ativo (útil para queries globais)"""
        cls._current_tenant_id = None

    @classmethod
    @asynccontextmanager
    async def scope(cls, tenant_id: int):
        """Context manager para executar código dentro de um escopo de tenant"""
        previous_tenant = cls._current_tenant_id
        cls.set_tenant(tenant_id)
        try:
            yield
        finally:
            cls._current_tenant_id = previous_tenant


def apply_tenant_filter(query, model_class):
    """
    Aplica filtro de tenant automaticamente em queries
    A ser usado via event listeners do SQLAlchemy
    """
    tenant_id = TenantScope.get_tenant()
    if tenant_id is not None and hasattr(model_class, "tenant_id"):
        # Filtra automaticamente por tenant_id se o modelo tiver essa coluna
        return query.filter(model_class.tenant_id == tenant_id)
    return query

