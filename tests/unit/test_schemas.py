"""
Unit Tests - API Schemas
"""
import pytest
from pydantic import ValidationError

from src.api.schemas import (
    ChatRequest,
    ChatResponse,
    UserProfileCreate,
    UserProfileUpdate,
    BiometricsInput,
    BrandPerformanceResponse,
)


def test_chat_request_valid():
    """Testa ChatRequest com dados válidos"""
    request = ChatRequest(
        user_input="Qual whey protein é melhor?",
        user_profile_id=1,
        session_id="test-session",
    )
    assert request.user_input == "Qual whey protein é melhor?"
    assert request.user_profile_id == 1
    assert request.session_id == "test-session"


def test_chat_request_minimal():
    """Testa ChatRequest com apenas campo obrigatório"""
    request = ChatRequest(user_input="Test input")
    assert request.user_input == "Test input"
    assert request.user_profile_id is None
    assert request.session_id is None


def test_biometrics_input_valid():
    """Testa BiometricsInput com dados válidos"""
    biometrics = BiometricsInput(
        weight_kg=75.5,
        height_cm=175,
        age=30,
        sex="male",
    )
    assert biometrics.weight_kg == 75.5
    assert biometrics.height_cm == 175
    assert biometrics.age == 30
    assert biometrics.sex == "male"


def test_biometrics_input_invalid_weight():
    """Testa BiometricsInput com peso inválido"""
    with pytest.raises(ValidationError):
        BiometricsInput(
            weight_kg=-10,  # Inválido: peso deve ser > 0
            height_cm=175,
            age=30,
            sex="male",
        )


def test_biometrics_input_invalid_age():
    """Testa BiometricsInput com idade inválida"""
    with pytest.raises(ValidationError):
        BiometricsInput(
            weight_kg=75.5,
            height_cm=175,
            age=150,  # Inválido: idade deve ser <= 120
            sex="male",
        )


def test_biometrics_input_invalid_sex():
    """Testa BiometricsInput com sexo inválido"""
    with pytest.raises(ValidationError):
        BiometricsInput(
            weight_kg=75.5,
            height_cm=175,
            age=30,
            sex="invalid",  # Inválido: deve ser male|female|other
        )


def test_user_profile_create_valid():
    """Testa UserProfileCreate com dados válidos"""
    from src.domain.enums import UserGoal, BudgetRange, DietaryRestriction, MedicalCondition
    
    profile = UserProfileCreate(
        biometrics=BiometricsInput(
            weight_kg=75.5,
            height_cm=175,
            age=30,
            sex="male",
        ),
        goal=UserGoal.MUSCLE_GAIN,
        dietary_restrictions=[DietaryRestriction.LACTOSE_FREE],
        medical_conditions=[MedicalCondition.DIABETES],
        budget_range=BudgetRange.MEDIUM,
    )
    assert profile.goal == UserGoal.MUSCLE_GAIN
    assert len(profile.dietary_restrictions) == 1
    assert len(profile.medical_conditions) == 1


def test_user_profile_update_all_optional():
    """Testa UserProfileUpdate com todos campos opcionais"""
    update = UserProfileUpdate()
    assert update.biometrics is None
    assert update.goal is None
    assert update.dietary_restrictions is None
    assert update.medical_conditions is None
    assert update.budget_range is None


def test_brand_performance_response():
    """Testa BrandPerformanceResponse"""
    response = BrandPerformanceResponse(
        brand_name="Growth",
        product_name="Whey Protein",
        recommendation_count=45,
        avg_satisfaction=4.5,
        total_selections=20,
        conversion_rate=0.4444,
    )
    assert response.brand_name == "Growth"
    assert response.recommendation_count == 45
    assert response.conversion_rate == 0.4444

