#!/usr/bin/env python3
"""
Seed Demo Tenant
Cria tenant demo e produtos de marcas reais concorrentes
com tabelas nutricionais reais para teste de comparação
"""
import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infrastructure.seeders.base import BaseSeeder
from src.infrastructure.seeders.utils import get_or_create
from src.domain.models import Tenant, Product
from src.domain.enums import TenantPlan, SupplementCategory


class DemoTenantSeeder(BaseSeeder):
    """Seeder para tenant demo com produtos reais"""

    def seed(self) -> None:
        """Popula tenant demo e produtos de marcas reais"""
        if not self.session:
            raise RuntimeError("Session não inicializada. Use context manager.")

        print("🌱 Criando tenant demo e produtos de marcas reais...")

        # Criar tenant demo
        tenant, tenant_created = get_or_create(
            self.session,
            Tenant,
            name="Loja Demo - Academia Fit",
            defaults={"plan": TenantPlan.PRO}
        )
        # Garantir que tenant foi commitado e tem ID
        if tenant_created:
            self.session.commit()
        self.session.refresh(tenant)
        print(f"{'✅ Criado' if tenant_created else '⚠️  Já existe'} tenant: {tenant.name} (ID: {tenant.id})")

        # Produtos reais de marcas concorrentes - Whey Protein
        # Dados baseados em tabelas nutricionais reais de marcas populares no Brasil
        products = [
            {
                "tenant_id": tenant.id,
                "brand_name": "Growth Supplements",
                "product_name": "Whey Protein Concentrado",
                "category": SupplementCategory.PROTEIN,
                "nutritional_info": {
                    "protein_g": 24.0,
                    "carbs_g": 3.5,
                    "fat_g": 1.8,
                    "calories": 120,
                    "serving_size_g": 30,
                    "ingredients": [
                        "Whey Protein Concentrate",
                        "Cacau em Pó",
                        "Aromatizante Artificial",
                        "Sucralose",
                        "Xanthan Gum"
                    ],
                    "allergens": ["Leite"],
                    "no_gluten": True,
                    "no_lactose": False,
                    "vegan": False,
                    "maltodextrin": False,
                    "artificial_sweeteners": True,
                    "added_sugars_g": 0.0,
                    "sodium_mg": 50.0
                },
                "certifications": ["ANVISA", "GMP"],
                "price": 89.90,
                "currency": "BRL",
                "stock_quantity": 50,
                "is_active": True
            },
            {
                "tenant_id": tenant.id,
                "brand_name": "Max Titanium",
                "product_name": "Whey 3W - Whey Protein Blend",
                "category": SupplementCategory.PROTEIN,
                "nutritional_info": {
                    "protein_g": 23.0,
                    "carbs_g": 4.0,
                    "fat_g": 2.0,
                    "calories": 120,
                    "serving_size_g": 30,
                    "ingredients": [
                        "Whey Protein Concentrate",
                        "Whey Protein Isolate",
                        "Whey Protein Hydrolyzed",
                        "Cacau em Pó",
                        "Aromatizante",
                        "Maltodextrina",
                        "Açúcar",
                        "Aspartame"
                    ],
                    "allergens": ["Leite"],
                    "no_gluten": True,
                    "no_lactose": False,
                    "vegan": False,
                    "maltodextrin": True,
                    "artificial_sweeteners": True,
                    "added_sugars_g": 2.0,
                    "sodium_mg": 65.0
                },
                "certifications": ["ANVISA"],
                "price": 99.90,
                "currency": "BRL",
                "stock_quantity": 30,
                "is_active": True
            },
            {
                "tenant_id": tenant.id,
                "brand_name": "IntegralMedica",
                "product_name": "Whey Zero Lactose",
                "category": SupplementCategory.PROTEIN,
                "nutritional_info": {
                    "protein_g": 25.0,
                    "carbs_g": 2.0,
                    "fat_g": 1.5,
                    "calories": 110,
                    "serving_size_g": 30,
                    "ingredients": [
                        "Whey Protein Isolate",
                        "Cacau em Pó",
                        "Stevia",
                        "Lecitina de Soja"
                    ],
                    "allergens": ["Leite"],
                    "no_gluten": True,
                    "no_lactose": True,
                    "vegan": False,
                    "maltodextrin": False,
                    "artificial_sweeteners": False,
                    "added_sugars_g": 0.0,
                    "sodium_mg": 40.0
                },
                "certifications": ["ANVISA", "GMP", "SEM LACTOSE"],
                "price": 129.90,
                "currency": "BRL",
                "stock_quantity": 25,
                "is_active": True
            },
            {
                "tenant_id": tenant.id,
                "brand_name": "Dux Nutrition",
                "product_name": "Whey Protein Isolado",
                "category": SupplementCategory.PROTEIN,
                "nutritional_info": {
                    "protein_g": 26.0,
                    "carbs_g": 1.0,
                    "fat_g": 1.0,
                    "calories": 105,
                    "serving_size_g": 30,
                    "ingredients": [
                        "Whey Protein Isolate",
                        "Cacau em Pó",
                        "Aromatizante Natural",
                        "Stevia",
                        "Xanthan Gum"
                    ],
                    "allergens": ["Leite"],
                    "no_gluten": True,
                    "no_lactose": False,
                    "vegan": False,
                    "maltodextrin": False,
                    "artificial_sweeteners": False,
                    "added_sugars_g": 0.0,
                    "sodium_mg": 35.0
                },
                "certifications": ["ANVISA", "GMP"],
                "price": 149.90,
                "currency": "BRL",
                "stock_quantity": 20,
                "is_active": True
            },
            {
                "tenant_id": tenant.id,
                "brand_name": "Growth Supplements",
                "product_name": "Creatina Monohidratada",
                "category": SupplementCategory.CREATINE,
                "nutritional_info": {
                    "protein_g": 0.0,
                    "carbs_g": 0.0,
                    "fat_g": 0.0,
                    "calories": 0,
                    "serving_size_g": 5,
                    "creatine_g": 5.0,
                    "ingredients": ["Creatine Monohydrate"],
                    "allergens": [],
                    "no_gluten": True,
                    "no_lactose": True,
                    "vegan": True,
                    "maltodextrin": False,
                    "artificial_sweeteners": False,
                    "added_sugars_g": 0.0,
                    "sodium_mg": 0.0
                },
                "certifications": ["ANVISA", "GMP"],
                "price": 49.90,
                "currency": "BRL",
                "stock_quantity": 40,
                "is_active": True
            },
            {
                "tenant_id": tenant.id,
                "brand_name": "Max Titanium",
                "product_name": "Creatina Creapure",
                "category": SupplementCategory.CREATINE,
                "nutritional_info": {
                    "protein_g": 0.0,
                    "carbs_g": 0.0,
                    "fat_g": 0.0,
                    "calories": 0,
                    "serving_size_g": 5,
                    "creatine_g": 5.0,
                    "ingredients": ["Creatine Monohydrate (Creapure)"],
                    "allergens": [],
                    "no_gluten": True,
                    "no_lactose": True,
                    "vegan": True,
                    "maltodextrin": False,
                    "artificial_sweeteners": False,
                    "added_sugars_g": 0.0,
                    "sodium_mg": 0.0
                },
                "certifications": ["ANVISA", "GMP", "Creapure"],
                "price": 69.90,
                "currency": "BRL",
                "stock_quantity": 35,
                "is_active": True
            },
            {
                "tenant_id": tenant.id,
                "brand_name": "IntegralMedica",
                "product_name": "Whey Vegan (Proteína de Ervilha)",
                "category": SupplementCategory.PROTEIN,
                "nutritional_info": {
                    "protein_g": 22.0,
                    "carbs_g": 4.0,
                    "fat_g": 2.0,
                    "calories": 115,
                    "serving_size_g": 30,
                    "ingredients": [
                        "Proteína de Ervilha Isolada",
                        "Cacau em Pó",
                        "Stevia",
                        "Lecitina de Girassol"
                    ],
                    "allergens": [],
                    "no_gluten": True,
                    "no_lactose": True,
                    "vegan": True,
                    "maltodextrin": False,
                    "artificial_sweeteners": False,
                    "added_sugars_g": 0.0,
                    "sodium_mg": 120.0
                },
                "certifications": ["ANVISA", "VEGAN", "SEM LACTOSE"],
                "price": 119.90,
                "currency": "BRL",
                "stock_quantity": 15,
                "is_active": True
            }
        ]

        created_count = 0
        skipped_count = 0

        for product_data in products:
            instance, created = get_or_create(
                self.session,
                Product,
                tenant_id=product_data["tenant_id"],
                brand_name=product_data["brand_name"],
                product_name=product_data["product_name"],
                defaults=product_data
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.session.commit()

        print(f"✅ Produtos populados:")
        print(f"   - Criados: {created_count}")
        print(f"   - Já existentes: {skipped_count}")
        print(f"   - Total: {len(products)}")
        print(f"\n📦 Produtos criados para comparação técnica:")
        for product_data in products:
            print(f"   - {product_data['brand_name']} - {product_data['product_name']} (R$ {product_data['price']})")


def main() -> None:
    """Função principal do script"""
    with DemoTenantSeeder() as seeder:
        seeder.seed()


if __name__ == "__main__":
    main()

