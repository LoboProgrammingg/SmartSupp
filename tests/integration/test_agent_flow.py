"""
Integration Tests - Agent Flow Completo
"""
import pytest
from src.agents.runner import run_agent
from src.domain.enums import UserGoal, BudgetRange, DietaryRestriction, MedicalCondition


@pytest.mark.asyncio
async def test_agent_complete_flow(
    test_session,
    sample_tenant,
    sample_user_profile,
    sample_products,
    sample_scientific_data,
):
    """Testa fluxo completo do agente"""
    result = await run_agent(
        user_input="Qual whey protein é melhor para mim?",
        tenant_id=sample_tenant.id,
        user_profile_id=sample_user_profile.id,
        session=test_session,
    )
    
    # Verificar que todos os steps foram executados
    assert result["step"] == "analytics_logged" or "error" not in result.get("errors", [])
    assert result["response"] is not None
    assert result["session_id"] is not None
    
    # Verificar que dados foram coletados
    assert result.get("goal") == UserGoal.MUSCLE_GAIN.value
    assert result.get("recommended_category") is not None
    assert result.get("scientific_data") is not None
    assert result.get("ranked_products") is not None


@pytest.mark.asyncio
async def test_agent_without_profile(
    test_session,
    sample_tenant,
    sample_products,
    sample_scientific_data,
):
    """Testa agente sem perfil de usuário"""
    # Estado inicial com dados básicos
    from src.agents.graph import get_graph
    from src.agents.state import AgentState
    
    initial_state: AgentState = {
        "session_id": "test-session",
        "tenant_id": sample_tenant.id,
        "user_profile_id": None,
        "user_input": "Qual whey protein é melhor?",
        "query_text": "Qual whey protein é melhor?",
        "biometrics": {"weight_kg": 75.5, "height_cm": 175, "age": 30, "sex": "male"},
        "goal": UserGoal.MUSCLE_GAIN.value,
        "dietary_restrictions": [],
        "medical_conditions": [],
        "budget_range": BudgetRange.MEDIUM.value,
        "scientific_data": None,
        "recommended_category": None,
        "available_products": None,
        "filtered_products": None,
        "ranked_products": None,
        "ranking_data": None,
        "response": None,
        "explanation": None,
        "recommended_product_ids": None,
        "errors": None,
        "step": "initialized",
    }
    
    graph = get_graph()
    config = {"configurable": {"session": test_session}}
    
    result = await graph.ainvoke(initial_state, config=config)
    
    # Deve processar mesmo sem perfil se dados básicos estiverem presentes
    assert result["step"] in ["analytics_logged", "response_generated", "response_generated_fallback"]
    assert result.get("response") is not None


@pytest.mark.asyncio
async def test_agent_error_handling(test_session, sample_tenant):
    """Testa tratamento de erros do agente"""
    # Executar com tenant inexistente
    result = await run_agent(
        user_input="Test",
        tenant_id=99999,  # Tenant inexistente
        user_profile_id=None,
        session=test_session,
    )
    
    # Deve retornar resultado mesmo com erro
    assert "response" in result
    assert result.get("step") in ["error", "analytics_logged"] or "errors" in result

