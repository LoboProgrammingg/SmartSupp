"""
Base Seeder Class
Classe base reutilizável para seeding de dados
"""
from typing import Any
from sqlmodel import Session
from src.core.database import sync_engine


class BaseSeeder:
    """Classe base para seeders - DRY principle"""

    def __init__(self):
        self.session: Session | None = None

    def __enter__(self):
        """Context manager entry"""
        self.session = Session(sync_engine)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        """Context manager exit - commit ou rollback"""
        if self.session:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
            self.session.close()
        return False

    def seed(self) -> None:
        """Método principal de seeding - deve ser implementado pelas subclasses"""
        raise NotImplementedError("Subclasses devem implementar seed()")

