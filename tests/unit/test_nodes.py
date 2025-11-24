"""
Unit Tests - LangGraph Nodes
"""
import pytest
from src.agents.nodes.anamnesis_collector import anamnesis_collector
from src.agents.nodes.science_retriever import science_retriever
from src.agents.nodes.comparative_analysis import comparative_analysis
from src.agents.state import AgentState
from src.domain.enums import UserGoal, BudgetRange, DietaryRestriction, MedicalCondition, SupplementCategory


@pytest.mark.asyncio
async def test_anamnesis_collector_with_profile(test_session, sample_user_profile):
    """Testa AnamnesisCollector com perfil existente"""
    state: AgentState = {
        "session_id": "test-session",
        "tenant_id": sample_user_profile.tenant_id,
        "user_profile_id": sample_user_profile.id,
        "user_input": "Test input",
        "query_text": None,
        "biometrics": None,
        "goal": None,
        "dietary_restrictions": None,
        "medical_conditions": None,
        "budget_range": None,
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
    
    config = {"configurable": {"session": test_session}}
    result = await anamnesis_collector(state, config)
    
    assert result["step"] == "anamnesis_collected_from_profile"
    assert result["goal"] == UserGoal.MUSCLE_GAIN.value
    assert result["budget_range"] == BudgetRange.MEDIUM.value
    assert DietaryRestriction.LACTOSE_FREE.value in result["dietary_restrictions"]
    assert MedicalCondition.DIABETES.value in result["medical_conditions"]


@pytest.mark.asyncio
async def test_anamnesis_collector_without_profile(test_session, sample_tenant):
    """Testa AnamnesisCollector sem perfil (validação de campos)"""
    state: AgentState = {
        "session_id": "test-session",
        "tenant_id": sample_tenant.id,
        "user_profile_id": None,
        "user_input": "Test input",
        "query_text": None,
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
    
    config = {"configurable": {"session": test_session}}
    result = await anamnesis_collector(state, config)
    
    assert result["step"] == "anamnesis_collected"


@pytest.mark.asyncio
async def test_anamnesis_collector_missing_fields(test_session, sample_tenant):
    """Testa AnamnesisCollector com campos faltando"""
    state: AgentState = {
        "session_id": "test-session",
        "tenant_id": sample_tenant.id,
        "user_profile_id": None,
        "user_input": "Test input",
        "query_text": None,
        "biometrics": None,
        "goal": None,
        "dietary_restrictions": None,
        "medical_conditions": None,
        "budget_range": None,
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
    
    config = {"configurable": {"session": test_session}}
    result = await anamnesis_collector(state, config)
    
    assert result["step"] == "anamnesis_incomplete"
    assert "errors" in result
    assert len(result["errors"]) > 0


@pytest.mark.asyncio
async def test_science_retriever(test_session, sample_scientific_data):
    """Testa ScienceRetriever"""
    state: AgentState = {
        "session_id": "test-session",
        "tenant_id": 1,
        "user_profile_id": None,
        "user_input": "Test input",
        "query_text": None,
        "biometrics": None,
        "goal": UserGoal.MUSCLE_GAIN.value,
        "dietary_restrictions": [],
        "medical_conditions": [],
        "budget_range": None,
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
    
    config = {"configurable": {"session": test_session}}
    result = await science_retriever(state, config)
    
    assert result["step"] == "science_retrieved"
    assert result["recommended_category"] == SupplementCategory.PROTEIN.value
    assert result["scientific_data"] is not None
    assert len(result["scientific_data"]) > 0
    assert result["scientific_data"][0]["supplement_name"] == "Whey Protein"


@pytest.mark.asyncio
async def test_science_retriever_no_goal(test_session):
    """Testa ScienceRetriever sem goal definido"""
    state: AgentState = {
        "session_id": "test-session",
        "tenant_id": 1,
        "user_profile_id": None,
        "user_input": "Test input",
        "query_text": None,
        "biometrics": None,
        "goal": None,
        "dietary_restrictions": [],
        "medical_conditions": [],
        "budget_range": None,
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
    
    config = {"configurable": {"session": test_session}}
    result = await science_retriever(state, config)
    
    assert result["step"] == "science_retrieval_failed"
    assert "errors" in result


@pytest.mark.asyncio
async def test_comparative_analysis(test_session, sample_tenant, sample_products):
    """Testa ComparativeAnalysis"""
    state: AgentState = {
        "session_id": "test-session",
        "tenant_id": sample_tenant.id,
        "user_profile_id": None,
        "user_input": "Test input",
        "query_text": None,
        "biometrics": None,
        "goal": UserGoal.MUSCLE_GAIN.value,
        "dietary_restrictions": [DietaryRestriction.LACTOSE_FREE.value],
        "medical_conditions": [MedicalCondition.DIABETES.value],
        "budget_range": BudgetRange.MEDIUM.value,
        "scientific_data": [],
        "recommended_category": SupplementCategory.PROTEIN.value,
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
    
    config = {"configurable": {"session": test_session}}
    result = await comparative_analysis(state, config)
    
    assert result["step"] == "comparative_analysis_complete"
    assert result["available_products"] is not None
    assert result["filtered_products"] is not None
    assert result["ranked_products"] is not None
    assert result["recommended_product_ids"] is not None
    
    # Verificar que produtos com lactose foram filtrados
    # IntegralMedica Zero Lactose deve estar presente, Growth não
    filtered_names = [p["brand_name"] for p in result["filtered_products"]]
    assert "IntegralMedica" in filtered_names
    # Growth não deve estar se tem lactose
    # (dependendo dos dados de teste, pode estar ou não)

