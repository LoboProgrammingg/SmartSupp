"""
API Schemas - Pydantic Models para validação de requests e responses
"""
from typing import Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from src.domain.enums import (
    UserGoal,
    BudgetRange,
    DietaryRestriction,
    MedicalCondition,
)


# ============================================================================
# Chat/Recommendation Schemas
# ============================================================================

class ChatRequest(BaseModel):
    """Request para endpoint POST /chat"""
    user_input: str = Field(..., description="Input do usuário (pergunta/requisição)")
    user_profile_id: Optional[int] = Field(None, description="ID do perfil do usuário (opcional)")
    session_id: Optional[str] = Field(None, description="ID da sessão (opcional)")


class ChatResponse(BaseModel):
    """Response do endpoint POST /chat"""
    response: str = Field(..., description="Resposta gerada pelo agente")
    explanation: Optional[str] = Field(None, description="Explicação detalhada")
    recommended_product_ids: list[int] = Field(default_factory=list, description="IDs dos produtos recomendados")
    ranking_data: Optional[dict[str, Any]] = Field(None, description="Dados de ranqueamento")
    session_id: str = Field(..., description="ID da sessão")
    step: str = Field(..., description="Último step executado")


# ============================================================================
# User Profile Schemas
# ============================================================================

class BiometricsInput(BaseModel):
    """Dados biométricos do usuário"""
    weight_kg: float = Field(..., gt=0, description="Peso em kg")
    height_cm: float = Field(..., gt=0, description="Altura em cm")
    age: int = Field(..., gt=0, le=120, description="Idade em anos")
    sex: str = Field(..., pattern="^(male|female|other)$", description="Sexo")


class UserProfileCreate(BaseModel):
    """Request para criar perfil de usuário"""
    biometrics: BiometricsInput = Field(..., description="Dados biométricos")
    goal: UserGoal = Field(..., description="Objetivo do usuário")
    dietary_restrictions: list[DietaryRestriction] = Field(
        default_factory=list,
        description="Restrições alimentares"
    )
    medical_conditions: list[MedicalCondition] = Field(
        default_factory=list,
        description="Condições médicas"
    )
    budget_range: BudgetRange = Field(..., description="Faixa de orçamento")


class UserProfileUpdate(BaseModel):
    """Request para atualizar perfil de usuário"""
    biometrics: Optional[BiometricsInput] = Field(None, description="Dados biométricos")
    goal: Optional[UserGoal] = Field(None, description="Objetivo do usuário")
    dietary_restrictions: Optional[list[DietaryRestriction]] = Field(
        None,
        description="Restrições alimentares"
    )
    medical_conditions: Optional[list[MedicalCondition]] = Field(
        None,
        description="Condições médicas"
    )
    budget_range: Optional[BudgetRange] = Field(None, description="Faixa de orçamento")


class UserProfileResponse(BaseModel):
    """Response do perfil de usuário"""
    id: int
    tenant_id: int
    biometrics: dict[str, Any]
    goal: str
    dietary_restrictions: list[str]
    medical_conditions: list[str]
    budget_range: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ============================================================================
# Analytics Schemas
# ============================================================================

class BrandPerformanceResponse(BaseModel):
    """Response do endpoint GET /analytics/brand-performance"""
    brand_name: str
    product_name: str
    recommendation_count: int
    avg_satisfaction: Optional[float]
    total_selections: int
    conversion_rate: float  # selections / recommendations


class AnalyticsResponse(BaseModel):
    """Response geral de analytics"""
    tenant_id: int
    period_start: datetime
    period_end: datetime
    total_interactions: int
    brand_performance: list[BrandPerformanceResponse]

