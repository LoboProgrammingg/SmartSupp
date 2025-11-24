"""
Pytest Configuration and Fixtures
Fixtures compartilhadas para todos os testes
"""
import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from fastapi.testclient import TestClient

from src.core.database import SQLModel
from src.core.config import settings
from src.main import app
from src.domain.models import Tenant, UserProfile, Product, ScientificData, InteractionLog
from src.domain.enums import TenantPlan, UserGoal, BudgetRange, DietaryRestriction, MedicalCondition, SupplementCategory, EvidenceLevel


# Database de teste (usar banco separado ou SQLite em memória)
TEST_DATABASE_URL = "postgresql+asyncpg://test:test@localhost:5432/smartsupp_test"


@pytest.fixture(scope="session")
def test_engine():
    """Engine de teste para criar banco"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    return engine


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db(test_engine):
    """Cria e destroi schema de teste"""
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield
    
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Sessão de teste isolada por teste"""
    async_session = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def test_client() -> TestClient:
    """Cliente de teste FastAPI"""
    return TestClient(app)


@pytest.fixture
async def sample_tenant(test_session: AsyncSession) -> Tenant:
    """Tenant de teste"""
    tenant = Tenant(
        name="Test Tenant",
        plan=TenantPlan.PRO,
    )
    test_session.add(tenant)
    await test_session.commit()
    await test_session.refresh(tenant)
    return tenant


@pytest.fixture
async def sample_user_profile(test_session: AsyncSession, sample_tenant: Tenant) -> UserProfile:
    """Perfil de usuário de teste"""
    profile = UserProfile(
        tenant_id=sample_tenant.id,
        biometrics={
            "weight_kg": 75.5,
            "height_cm": 175,
            "age": 30,
            "sex": "male",
            "bmi": 24.7,
        },
        goal=UserGoal.MUSCLE_GAIN,
        dietary_restrictions=[DietaryRestriction.LACTOSE_FREE],
        medical_conditions=[MedicalCondition.DIABETES],
        budget_range=BudgetRange.MEDIUM,
    )
    test_session.add(profile)
    await test_session.commit()
    await test_session.refresh(profile)
    return profile


@pytest.fixture
async def sample_scientific_data(test_session: AsyncSession) -> ScientificData:
    """Dados científicos de teste"""
    science = ScientificData(
        supplement_name="Whey Protein",
        category=SupplementCategory.PROTEIN,
        evidence_level=EvidenceLevel.STRONG,
        source="AIS",
        effects={"muscle_gain": "strong", "strength": "strong"},
        dosage={"min": 20.0, "max": 40.0, "unit": "g", "timing": "post_workout"},
        contraindications=["kidney_disease"],
        interactions={},
    )
    test_session.add(science)
    await test_session.commit()
    await test_session.refresh(science)
    return science


@pytest.fixture
async def sample_products(test_session: AsyncSession, sample_tenant: Tenant) -> list[Product]:
    """Produtos de teste"""
    products = [
        Product(
            tenant_id=sample_tenant.id,
            brand_name="Growth",
            product_name="Whey Protein",
            category=SupplementCategory.PROTEIN,
            nutritional_info={
                "protein_g": 24.0,
                "carbs_g": 3.5,
                "fat_g": 1.8,
                "calories": 120,
                "serving_size_g": 30,
                "no_lactose": False,
                "maltodextrin": False,
                "vegan": False,
                "artificial_sweeteners": True,
            },
            certifications=["ANVISA", "GMP"],
            price=89.90,
            stock_quantity=50,
            is_active=True,
        ),
        Product(
            tenant_id=sample_tenant.id,
            brand_name="IntegralMedica",
            product_name="Whey Zero Lactose",
            category=SupplementCategory.PROTEIN,
            nutritional_info={
                "protein_g": 25.0,
                "carbs_g": 2.0,
                "fat_g": 1.5,
                "calories": 110,
                "serving_size_g": 30,
                "no_lactose": True,
                "maltodextrin": False,
                "vegan": False,
                "artificial_sweeteners": False,
            },
            certifications=["ANVISA", "GMP", "SEM LACTOSE"],
            price=129.90,
            stock_quantity=25,
            is_active=True,
        ),
    ]
    
    for product in products:
        test_session.add(product)
    
    await test_session.commit()
    
    for product in products:
        await test_session.refresh(product)
    
    return products

