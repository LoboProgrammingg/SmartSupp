"""
User Profile Routes
POST /user-profile - Criar/atualizar perfil de usuário
GET /user-profile/{profile_id} - Buscar perfil
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.api.schemas import (
    UserProfileCreate,
    UserProfileUpdate,
    UserProfileResponse,
)
from src.api.dependencies import get_db_session, get_tenant_id_from_header
from src.domain.models import UserProfile
from src.domain.enums import UserGoal, BudgetRange

router = APIRouter(prefix="/user-profile", tags=["user-profile"])


@router.post("", response_model=UserProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_user_profile(
    profile_data: UserProfileCreate,
    tenant_id: int = Depends(get_tenant_id_from_header),
    session: AsyncSession = Depends(get_db_session),
) -> UserProfileResponse:
    """
    Criar novo perfil de usuário
    """
    # Calcular BMI
    bmi = profile_data.biometrics.weight_kg / (
        (profile_data.biometrics.height_cm / 100) ** 2
    )

    biometrics = {
        "weight_kg": profile_data.biometrics.weight_kg,
        "height_cm": profile_data.biometrics.height_cm,
        "age": profile_data.biometrics.age,
        "sex": profile_data.biometrics.sex,
        "bmi": round(bmi, 2),
    }

    profile = UserProfile(
        tenant_id=tenant_id,
        biometrics=biometrics,
        goal=profile_data.goal,
        dietary_restrictions=profile_data.dietary_restrictions,
        medical_conditions=profile_data.medical_conditions,
        budget_range=profile_data.budget_range,
    )

    session.add(profile)
    await session.commit()
    await session.refresh(profile)

    return UserProfileResponse.model_validate(profile)


@router.get("/{profile_id}", response_model=UserProfileResponse)
async def get_user_profile(
    profile_id: int,
    tenant_id: int = Depends(get_tenant_id_from_header),
    session: AsyncSession = Depends(get_db_session),
) -> UserProfileResponse:
    """
    Buscar perfil de usuário por ID
    """
    stmt = (
        select(UserProfile)
        .where(UserProfile.id == profile_id)
        .where(UserProfile.tenant_id == tenant_id)
    )
    profile = (await session.exec(stmt)).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Perfil {profile_id} não encontrado",
        )

    return UserProfileResponse.model_validate(profile)


@router.put("/{profile_id}", response_model=UserProfileResponse)
async def update_user_profile(
    profile_id: int,
    profile_data: UserProfileUpdate,
    tenant_id: int = Depends(get_tenant_id_from_header),
    session: AsyncSession = Depends(get_db_session),
) -> UserProfileResponse:
    """
    Atualizar perfil de usuário existente
    """
    stmt = (
        select(UserProfile)
        .where(UserProfile.id == profile_id)
        .where(UserProfile.tenant_id == tenant_id)
    )
    profile = (await session.exec(stmt)).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Perfil {profile_id} não encontrado",
        )

    # Atualizar campos fornecidos
    if profile_data.biometrics:
        bmi = profile_data.biometrics.weight_kg / (
            (profile_data.biometrics.height_cm / 100) ** 2
        )
        profile.biometrics = {
            "weight_kg": profile_data.biometrics.weight_kg,
            "height_cm": profile_data.biometrics.height_cm,
            "age": profile_data.biometrics.age,
            "sex": profile_data.biometrics.sex,
            "bmi": round(bmi, 2),
        }

    if profile_data.goal:
        profile.goal = profile_data.goal

    if profile_data.dietary_restrictions is not None:
        profile.dietary_restrictions = profile_data.dietary_restrictions

    if profile_data.medical_conditions is not None:
        profile.medical_conditions = profile_data.medical_conditions

    if profile_data.budget_range:
        profile.budget_range = profile_data.budget_range

    await session.commit()
    await session.refresh(profile)

    return UserProfileResponse.model_validate(profile)

