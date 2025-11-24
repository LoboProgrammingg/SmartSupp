"""
Security Module - Autenticação, Autorização e Isolamento Multitenant
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.database import TenantScope, get_session

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer token authentication
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha plain corresponde ao hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gera hash da senha"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria JWT token com payload customizado"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decodifica e valida JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_tenant_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session),
) -> int:
    """
    Dependency que extrai tenant_id do token JWT
    E define o escopo de tenant para a requisição atual
    
    O token JWT deve conter:
    {
        "sub": "user_id",
        "tenant_id": 123,
        "email": "user@example.com"
    }
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    tenant_id: int | None = payload.get("tenant_id")
    if tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token não contém tenant_id",
        )
    
    # Define o escopo de tenant para esta requisição
    # Todas as queries subsequentes serão automaticamente filtradas
    TenantScope.set_tenant(tenant_id)
    
    return tenant_id


async def get_current_user_id(
    tenant_id: int = Depends(get_current_tenant_id),
) -> int:
    """
    Dependency que retorna o user_id do token JWT
    Requer autenticação e tenant válidos
    """
    # Em uma implementação completa, você buscaria o token novamente
    # ou passaria via contexto. Por ora, simplificamos.
    # TODO: Implementar contexto de request completo
    raise NotImplementedError("Implementar busca de user_id do token")


class TenantMiddleware:
    """
    Middleware para isolamento automático de tenant
    A ser integrado ao FastAPI via add_middleware
    """
    
    @staticmethod
    async def extract_tenant_from_header(request, call_next):
        """
        Extrai tenant_id do header X-Tenant-ID (para desenvolvimento/teste)
        Em produção, usar apenas JWT via get_current_tenant_id
        """
        tenant_header = request.headers.get("X-Tenant-ID")
        if tenant_header:
            try:
                tenant_id = int(tenant_header)
                TenantScope.set_tenant(tenant_id)
            except (ValueError, TypeError):
                pass
        
        response = await call_next(request)
        
        # Limpa o escopo após a requisição
        TenantScope.clear_tenant()
        
        return response

