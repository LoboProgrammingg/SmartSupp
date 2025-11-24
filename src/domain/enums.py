"""
Domain Enums
Definições de tipos enumerados para o domínio
"""
from enum import Enum


class TenantPlan(str, Enum):
    """Planos disponíveis para tenants"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class UserGoal(str, Enum):
    """Objetivos do usuário"""
    WEIGHT_LOSS = "weight_loss"
    MUSCLE_GAIN = "muscle_gain"
    ENDURANCE = "endurance"
    GENERAL_HEALTH = "general_health"
    SPORTS_PERFORMANCE = "sports_performance"
    RECOVERY = "recovery"


class BudgetRange(str, Enum):
    """Faixas de orçamento do usuário"""
    LOW = "low"  # Até R$ 50
    MEDIUM = "medium"  # R$ 50 - R$ 150
    HIGH = "high"  # R$ 150 - R$ 300
    PREMIUM = "premium"  # Acima de R$ 300


class DietaryRestriction(str, Enum):
    """Restrições alimentares"""
    GLUTEN_FREE = "gluten_free"
    LACTOSE_FREE = "lactose_free"
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"
    KETO = "keto"
    PALEO = "paleo"
    NO_ARTIFICIAL_SWEETENERS = "no_artificial_sweeteners"
    NO_SOY = "no_soy"


class MedicalCondition(str, Enum):
    """Condições médicas relevantes"""
    DIABETES = "diabetes"
    HYPERTENSION = "hypertension"
    GASTRITIS = "gastritis"
    KIDNEY_DISEASE = "kidney_disease"
    LIVER_DISEASE = "liver_disease"
    CARDIAC_CONDITIONS = "cardiac_conditions"
    ALLERGIES = "allergies"


class EvidenceLevel(str, Enum):
    """Níveis de evidência científica (AIS Group A = Strong Evidence)"""
    STRONG = "strong"  # AIS Group A / Examine High/Moderate + Very High Consistency
    MODERATE = "moderate"
    WEAK = "weak"
    INSUFFICIENT = "insufficient"


class SupplementCategory(str, Enum):
    """Categorias de suplementos"""
    PROTEIN = "protein"
    CREATINE = "creatine"
    BCAAS = "bcaas"
    PRE_WORKOUT = "pre_workout"
    POST_WORKOUT = "post_workout"
    MULTIVITAMIN = "multivitamin"
    OMEGA3 = "omega3"
    VITAMIN_D = "vitamin_d"
    MAGNESIUM = "magnesium"
    ZINC = "zinc"
    CAFFEINE = "caffeine"
    BETA_ALANINE = "beta_alanine"
    CITRULLINE = "citrulline"
    GLUTAMINE = "glutamine"

