"""
Seeder Utilities
Funções auxiliares reutilizáveis para seeding
"""
from typing import Any
from sqlmodel import Session, select


def get_or_create(
    session: Session,
    model_class: type,
    defaults: dict[str, Any] | None = None,
    **kwargs: Any
) -> tuple[Any, bool]:
    """
    Get or create pattern - DRY para evitar duplicatas
    Retorna (instance, created)
    """
    stmt = select(model_class).filter_by(**kwargs)
    instance = session.exec(stmt).first()
    
    if instance:
        return instance, False
    
    create_data = {**kwargs}
    if defaults:
        create_data.update(defaults)
    
    instance = model_class(**create_data)
    session.add(instance)
    return instance, True


def batch_create(
    session: Session,
    model_class: type,
    items: list[dict[str, Any]],
    unique_fields: list[str] | None = None
) -> int:
    """
    Cria múltiplos itens em batch
    Retorna quantidade de itens criados
    """
    created_count = 0
    
    for item_data in items:
        if unique_fields:
            # Verifica se já existe
            filter_dict = {field: item_data[field] for field in unique_fields if field in item_data}
            stmt = select(model_class).filter_by(**filter_dict)
            existing = session.exec(stmt).first()
            if existing:
                continue
        
        instance = model_class(**item_data)
        session.add(instance)
        created_count += 1
    
    return created_count

