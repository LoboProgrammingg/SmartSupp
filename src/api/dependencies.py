"""
API Dependencies
Dependencies reutilizáveis para FastAPI endpoints
"""
from typing import Optional
from fastapi import Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session, TenantScope
from src.core.config import settings


async def get_db_session() -> AsyncSession:
    """Dependency para sessão de banco assíncrona"""
    async for session in get_session():
        yield session


def get_tenant_id_from_header(x_tenant_id: Optional[int] = Header(None)) -> int:
    """
    Dependency para extrair tenant_id do header X-Tenant-ID
    Para desenvolvimento/teste (em produção usar JWT)
    """
    if not x_tenant_id:
        if settings.DEBUG:
            # Em debug, usar tenant demo padrão (ID 1)
            tenant_id = 1
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Header X-Tenant-ID obrigatório",
            )
    else:
        tenant_id = x_tenant_id

    # Define escopo de tenant
    TenantScope.set_tenant(tenant_id)
    return tenant_id

