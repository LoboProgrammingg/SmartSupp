"""
FastAPI Main Application
SmartSupp - SaaS Multitenant de Recomendação de Suplementos Esportivos
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.database import init_db
from src.core.security import TenantMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="API para recomendação inteligente de suplementos esportivos",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configurar origins em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Adicionar TenantMiddleware quando implementado
# app.middleware("http")(TenantMiddleware.extract_tenant_from_header)


@app.on_event("startup")
async def startup_event():
    """Inicializa banco de dados na startup"""
    # Em produção, usar Alembic migrations ao invés de create_all
    if settings.DEBUG:
        init_db()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "SmartSupp API",
        "version": settings.VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check detalhado"""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Implementar verificação real
    }

