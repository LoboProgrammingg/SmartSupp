"""
Anamnesis Collector Node
Coleta e valida dados de anamnese (peso, altura, objetivos, restrições)
"""
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.agents.state import AgentState
from src.agents.utils import get_session_from_config
from src.domain.models import UserProfile
from src.domain.enums import UserGoal, BudgetRange, DietaryRestriction, MedicalCondition


async def anamnesis_collector(state: AgentState, config: dict[str, Any] | None = None) -> AgentState:
    """
    Node: Anamnesis Collector
    Garante que todos os dados de anamnese estão coletados
    """
    errors = state.get("errors", [])
    session = get_session_from_config(config)

    # Se já existe user_profile_id, buscar perfil existente
    if state.get("user_profile_id") and session:
        stmt = select(UserProfile).where(UserProfile.id == state["user_profile_id"])
        profile = (await session.exec(stmt)).first()

        if profile:
            state["biometrics"] = profile.biometrics
            state["goal"] = profile.goal.value
            state["dietary_restrictions"] = [dr.value for dr in profile.dietary_restrictions]
            state["medical_conditions"] = [mc.value for mc in profile.medical_conditions]
            state["budget_range"] = profile.budget_range.value
            state["step"] = "anamnesis_collected_from_profile"
            return state

    # Se não há perfil, tentar extrair do user_input
    # Em produção, usar LLM para extração estruturada
    # Por ora, validar campos obrigatórios

    required_fields = ["biometrics", "goal", "budget_range"]
    missing_fields = [field for field in required_fields if not state.get(field)]

    if missing_fields:
        errors.append(f"Campos obrigatórios ausentes: {', '.join(missing_fields)}")
        state["errors"] = errors
        state["step"] = "anamnesis_incomplete"
        return state

    # Validar tipos
    if not isinstance(state.get("biometrics"), dict):
        errors.append("Biometrics deve ser um dicionário")

    if state.get("goal") not in [g.value for g in UserGoal]:
        errors.append(f"Goal inválido: {state.get('goal')}")

    if state.get("budget_range") not in [br.value for br in BudgetRange]:
        errors.append(f"Budget_range inválido: {state.get('budget_range')}")

    if errors:
        state["errors"] = errors
        state["step"] = "anamnesis_validation_failed"
        return state

    state["step"] = "anamnesis_collected"
    return state

