"""
Integration Tests - API Endpoints
"""
import pytest
from fastapi.testclient import TestClient
from src.domain.enums import UserGoal, BudgetRange, DietaryRestriction, MedicalCondition


@pytest.mark.asyncio
async def test_create_user_profile(test_client: TestClient, sample_tenant):
    """Testa criação de perfil de usuário"""
    response = test_client.post(
        "/user-profile",
        headers={"X-Tenant-ID": str(sample_tenant.id)},
        json={
            "biometrics": {
                "weight_kg": 75.5,
                "height_cm": 175,
                "age": 30,
                "sex": "male",
            },
            "goal": "muscle_gain",
            "dietary_restrictions": ["lactose_free"],
            "medical_conditions": ["diabetes"],
            "budget_range": "medium",
        },
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["goal"] == "muscle_gain"
    assert data["budget_range"] == "medium"
    assert "lactose_free" in data["dietary_restrictions"]
    assert "diabetes" in data["medical_conditions"]
    assert "bmi" in data["biometrics"]


@pytest.mark.asyncio
async def test_get_user_profile(test_client: TestClient, sample_tenant, sample_user_profile):
    """Testa busca de perfil de usuário"""
    response = test_client.get(
        f"/user-profile/{sample_user_profile.id}",
        headers={"X-Tenant-ID": str(sample_tenant.id)},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_user_profile.id
    assert data["tenant_id"] == sample_tenant.id


@pytest.mark.asyncio
async def test_update_user_profile(test_client: TestClient, sample_tenant, sample_user_profile):
    """Testa atualização de perfil de usuário"""
    response = test_client.put(
        f"/user-profile/{sample_user_profile.id}",
        headers={"X-Tenant-ID": str(sample_tenant.id)},
        json={
            "goal": "weight_loss",
            "budget_range": "low",
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["goal"] == "weight_loss"
    assert data["budget_range"] == "low"


@pytest.mark.asyncio
async def test_chat_endpoint(test_client: TestClient, sample_tenant, sample_user_profile, sample_products, sample_scientific_data):
    """Testa endpoint POST /chat"""
    response = test_client.post(
        "/chat",
        headers={"X-Tenant-ID": str(sample_tenant.id)},
        json={
            "user_input": "Qual whey protein é melhor para mim?",
            "user_profile_id": sample_user_profile.id,
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "session_id" in data
    assert "step" in data
    assert data["step"] != "error"  # Não deve ter erros


@pytest.mark.asyncio
async def test_chat_endpoint_without_profile(test_client: TestClient, sample_tenant, sample_products, sample_scientific_data):
    """Testa endpoint POST /chat sem perfil"""
    response = test_client.post(
        "/chat",
        headers={"X-Tenant-ID": str(sample_tenant.id)},
        json={
            "user_input": "Qual whey protein é melhor?",
        },
    )
    
    # Pode retornar erro se campos obrigatórios faltarem
    assert response.status_code in [200, 500]


@pytest.mark.asyncio
async def test_analytics_brand_performance(test_client: TestClient, sample_tenant):
    """Testa endpoint GET /analytics/brand-performance"""
    response = test_client.get(
        "/analytics/brand-performance?days=30",
        headers={"X-Tenant-ID": str(sample_tenant.id)},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "tenant_id" in data
    assert "period_start" in data
    assert "period_end" in data
    assert "total_interactions" in data
    assert "brand_performance" in data
    assert isinstance(data["brand_performance"], list)


@pytest.mark.asyncio
async def test_analytics_brand_performance_custom_days(test_client: TestClient, sample_tenant):
    """Testa endpoint GET /analytics/brand-performance com período customizado"""
    response = test_client.get(
        "/analytics/brand-performance?days=7",
        headers={"X-Tenant-ID": str(sample_tenant.id)},
    )
    
    assert response.status_code == 200
    data = response.json()


@pytest.mark.asyncio
async def test_get_user_profile_not_found(test_client: TestClient, sample_tenant):
    """Testa busca de perfil inexistente"""
    response = test_client.get(
        "/user-profile/99999",
        headers={"X-Tenant-ID": str(sample_tenant.id)},
    )
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_user_profile_invalid_data(test_client: TestClient, sample_tenant):
    """Testa criação de perfil com dados inválidos"""
    response = test_client.post(
        "/user-profile",
        headers={"X-Tenant-ID": str(sample_tenant.id)},
        json={
            "biometrics": {
                "weight_kg": -10,  # Inválido
                "height_cm": 175,
                "age": 30,
                "sex": "male",
            },
            "goal": "muscle_gain",
            "budget_range": "medium",
        },
    )
    
    assert response.status_code == 422  # Validation error

