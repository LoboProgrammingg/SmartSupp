"""
Domain Models (SQLModel)
Models de negócio com foco em comparação técnica de produtos
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column, JSON, ARRAY, String, Text
from sqlalchemy import Index

from src.domain.enums import (
    TenantPlan,
    UserGoal,
    BudgetRange,
    DietaryRestriction,
    MedicalCondition,
    EvidenceLevel,
    SupplementCategory,
)


# ============================================================================
# TENANT (Multitenancy)
# ============================================================================

class Tenant(SQLModel, table=True):
    """Tenant - Cliente/Loja que usa a plataforma"""
    __tablename__ = "tenants"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, index=True)
    plan: TenantPlan = Field(default=TenantPlan.FREE)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Índices
    __table_args__ = (
        Index("idx_tenant_name", "name"),
    )


# ============================================================================
# SCIENTIFIC DATA (GLOBAL - Sem tenant_id)
# ============================================================================

class ScientificData(SQLModel, table=True):
    """
    Dados científicos globais (AIS/Examine)
    Sem tenant_id - dados compartilhados por todos os tenants
    """
    __tablename__ = "scientific_data"

    id: Optional[int] = Field(default=None, primary_key=True)
    supplement_name: str = Field(max_length=255, index=True)
    category: SupplementCategory = Field(index=True)
    
    # Evidência Científica
    evidence_level: EvidenceLevel = Field(index=True)
    source: str = Field(max_length=100)  # "AIS" ou "Examine"
    source_url: Optional[str] = Field(default=None, max_length=500)
    
    # Efeitos e Benefícios (JSONB)
    effects: dict = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Efeitos documentados: {effect: strength_level}"
    )
    
    # Dosagem recomendada (JSONB)
    dosage: dict = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Dosagem: {min: float, max: float, unit: str, timing: str}"
    )
    
    # Contraindicações e Interações
    contraindications: list[str] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String)),
        description="Lista de condições que contraindica o uso"
    )
    
    interactions: dict = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Interações com medicamentos/condições: {medication: description}"
    )
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Índices para busca eficiente
    __table_args__ = (
        Index("idx_scientific_supplement", "supplement_name"),
        Index("idx_scientific_category", "category"),
        Index("idx_scientific_evidence", "evidence_level"),
        Index("idx_scientific_source", "source"),
    )


# ============================================================================
# USER PROFILE (Por Tenant)
# ============================================================================

class UserProfile(SQLModel, table=True):
    """
    Perfil do usuário - dados de anamnese
    tenant_id obrigatório - isolamento multitenant
    """
    __tablename__ = "user_profiles"

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenants.id", index=True)
    
    # Biometria (JSONB)
    biometrics: dict = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Dados vitais: {weight_kg: float, height_cm: float, age: int, sex: str, bmi: float}"
    )
    
    # Objetivo
    goal: UserGoal = Field(index=True)
    
    # Restrições alimentares
    dietary_restrictions: list[DietaryRestriction] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String)),
        description="Lista de restrições alimentares"
    )
    
    # Condições médicas
    medical_conditions: list[MedicalCondition] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String)),
        description="Lista de condições médicas relevantes"
    )
    
    # Orçamento
    budget_range: BudgetRange = Field(index=True)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Índices para queries frequentes
    __table_args__ = (
        Index("idx_user_tenant", "tenant_id"),
        Index("idx_user_goal", "goal"),
        Index("idx_user_budget", "budget_range"),
        Index("idx_user_tenant_goal", "tenant_id", "goal"),
    )


# ============================================================================
# PRODUCT (Por Tenant)
# ============================================================================

class Product(SQLModel, table=True):
    """
    Produto/Suplemento disponível no estoque do tenant
    tenant_id obrigatório - isolamento multitenant
    Foco em comparação técnica entre marcas
    """
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenants.id", index=True)
    
    # Identificação
    brand_name: str = Field(max_length=255, index=True)
    product_name: str = Field(max_length=255)
    category: SupplementCategory = Field(index=True)
    
    # Informações nutricionais (JSONB) - Crítico para comparação
    nutritional_info: dict = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Tabela nutricional: {protein_g: float, carbs_g: float, fat_g: float, calories: int, ingredients: list, allergens: list, ...}"
    )
    
    # Certificações e Qualidade
    certifications: list[str] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String)),
        description="Certificações: ['ANVISA', 'GMP', 'VEGAN', 'ORGANIC', ...]"
    )
    
    # Preço
    price: float = Field(index=True, description="Preço em R$")
    currency: str = Field(default="BRL", max_length=3)
    
    # Estoque
    stock_quantity: int = Field(default=0, index=True)
    is_active: bool = Field(default=True, index=True)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None, sa_column_kwargs={"onupdate": datetime.utcnow})

    # Índices para busca e comparação eficiente
    __table_args__ = (
        Index("idx_product_tenant", "tenant_id"),
        Index("idx_product_brand", "brand_name"),
        Index("idx_product_category", "category"),
        Index("idx_product_tenant_category", "tenant_id", "category"),
        Index("idx_product_active", "is_active", "tenant_id"),
        Index("idx_product_price", "price"),
    )


# ============================================================================
# INTERACTION LOG (BI - Por Tenant)
# ============================================================================

class InteractionLog(SQLModel, table=True):
    """
    Log de interações para BI e Analytics
    Registra cada consulta/recomendação realizada
    tenant_id obrigatório - isolamento multitenant
    """
    __tablename__ = "interaction_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenants.id", index=True)
    user_profile_id: Optional[int] = Field(default=None, foreign_key="user_profiles.id", index=True)
    
    # Contexto da interação
    session_id: str = Field(max_length=255, index=True)
    query_text: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Recomendações geradas
    recommended_products: list[int] = Field(
        default_factory=list,
        sa_column=Column(ARRAY(String)),
        description="IDs dos produtos recomendados"
    )
    
    # Ranking e Justificativas (JSONB)
    ranking_data: dict = Field(
        default_factory=dict,
        sa_column=Column(JSON),
        description="Dados de ranking: {product_id: {score: float, reasons: list, match_score: float}}"
    )
    
    # Produto selecionado (se houver)
    selected_product_id: Optional[int] = Field(default=None, foreign_key="products.id", index=True)
    
    # Feedback do usuário
    user_feedback: Optional[str] = Field(default=None, sa_column=Column(Text))
    satisfaction_score: Optional[int] = Field(default=None, description="Score de 1-5")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None, max_length=500)

    # Índices para análises de BI
    __table_args__ = (
        Index("idx_log_tenant", "tenant_id"),
        Index("idx_log_created", "created_at"),
        Index("idx_log_tenant_created", "tenant_id", "created_at"),
        Index("idx_log_selected", "selected_product_id"),
        Index("idx_log_session", "session_id"),
    )

