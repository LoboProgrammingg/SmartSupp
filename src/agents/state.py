"""
Agent State - TypedDict para LangGraph
Define o estado do agente durante o fluxo de recomendação
"""
from typing import TypedDict, Optional, Any
from uuid import UUID


class AgentState(TypedDict):
    """Estado do agente LangGraph - tipado com TypedDict"""

    # Identificação
    session_id: str
    tenant_id: int
    user_profile_id: Optional[int]

    # Input inicial
    user_input: str
    query_text: Optional[str]

    # Anamnese coletada
    biometrics: Optional[dict[str, Any]]
    goal: Optional[str]
    dietary_restrictions: Optional[list[str]]
    medical_conditions: Optional[list[str]]
    budget_range: Optional[str]

    # Dados científicos recuperados
    scientific_data: Optional[list[dict[str, Any]]]
    recommended_category: Optional[str]

    # Produtos e análise comparativa
    available_products: Optional[list[dict[str, Any]]]
    filtered_products: Optional[list[dict[str, Any]]]
    ranked_products: Optional[list[dict[str, Any]]]
    ranking_data: Optional[dict[str, dict[str, Any]]]

    # Resposta gerada
    response: Optional[str]
    explanation: Optional[str]
    recommended_product_ids: Optional[list[int]]

    # Metadata
    errors: Optional[list[str]]
    step: str  # Nome do último step executado

