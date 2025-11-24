#!/usr/bin/env python3
"""
Seed All - Executa todos os seeders
Script principal para popular banco de dados completo
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.seed_science import main as seed_science
from scripts.seed_demo_tenant import main as seed_demo_tenant


def main() -> None:
    """Executa todos os seeders em ordem"""
    print("=" * 60)
    print("🌱 SmartSupp - Seed All Scripts")
    print("=" * 60)
    print()

    try:
        # 1. Seed Scientific Data (global - sem tenant)
        print("📚 Passo 1/2: Dados Científicos (AIS/Examine)")
        seed_science()
        print()

        # 2. Seed Demo Tenant (com produtos reais)
        print("🏪 Passo 2/2: Tenant Demo e Produtos")
        seed_demo_tenant()
        print()

        print("=" * 60)
        print("✅ Seeding completo com sucesso!")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Erro durante seeding: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

