"""
Science Retriever Node
Busca dados científicos baseados no objetivo do usuário
"""
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.agents.state import AgentState
from src.agents.utils import get_session_from_config
from src.domain.models import ScientificData
from src.domain.enums import EvidenceLevel, SupplementCategory, UserGoal


# Mapeamento de objetivos para categorias de suplementos
GOAL_TO_CATEGORY: dict[str, SupplementCategory] = {
    UserGoal.MUSCLE_GAIN.value: SupplementCategory.PROTEIN,
    UserGoal.WEIGHT_LOSS.value: SupplementCategory.PROTEIN,
    UserGoal.ENDURANCE.value: SupplementCategory.CAFFEINE,
    UserGoal.SPORTS_PERFORMANCE.value: SupplementCategory.CREATINE,
    UserGoal.RECOVERY.value: SupplementCategory.PROTEIN,
    UserGoal.GENERAL_HEALTH.value: SupplementCategory.MULTIVITAMIN,
}


async def science_retriever(state: AgentState, config: dict[str, Any] | None = None) -> AgentState:
    """
    Node: Science Retriever
    Consulta base científica (AIS/Examine) baseado no objetivo
    """
    goal = state.get("goal")
    session = get_session_from_config(config)

    if not goal:
        state["errors"] = state.get("errors", []) + ["Goal não definido"]
        state["step"] = "science_retrieval_failed"
        return state

    if not session:
        state["errors"] = state.get("errors", []) + ["Sessão de banco não disponível"]
        state["step"] = "science_retrieval_failed"
        return state

    # Determinar categoria de suplemento baseado no objetivo
    category = GOAL_TO_CATEGORY.get(goal, SupplementCategory.PROTEIN)
    state["recommended_category"] = category.value

    # Buscar dados científicos (apenas STRONG evidence)
    stmt = (
        select(ScientificData)
        .where(ScientificData.category == category)
        .where(ScientificData.evidence_level == EvidenceLevel.STRONG)
    )
    results = (await session.exec(stmt)).all()

    scientific_data = [
        {
            "id": data.id,
            "supplement_name": data.supplement_name,
            "category": data.category.value,
            "evidence_level": data.evidence_level.value,
            "source": data.source,
            "effects": data.effects,
            "dosage": data.dosage,
            "contraindications": data.contraindications,
            "interactions": data.interactions,
        }
        for data in results
    ]

    state["scientific_data"] = scientific_data
    state["step"] = "science_retrieved"

    return state

