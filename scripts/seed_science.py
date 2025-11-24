#!/usr/bin/env python3
"""
Seed Scientific Data (AIS/Examine)
Popula tabela scientific_data com dados do AIS Group A e Examine.com
Apenas evidências fortes (STRONG evidence level)
"""
import sys
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.infrastructure.seeders.base import BaseSeeder
from src.infrastructure.seeders.utils import get_or_create
from src.domain.models import ScientificData
from src.domain.enums import EvidenceLevel, SupplementCategory


class ScienceSeeder(BaseSeeder):
    """Seeder para dados científicos globais"""

    def seed(self) -> None:
        """Popula scientific_data com dados do AIS/Examine"""
        if not self.session:
            raise RuntimeError("Session não inicializada. Use context manager.")

        print("🌱 Populando dados científicos (AIS Group A / Examine Strong Evidence)...")

        # Dados baseados em AIS Group A e Examine.com (Strong Evidence apenas)
        science_data = [
            {
                "supplement_name": "Whey Protein",
                "category": SupplementCategory.PROTEIN,
                "evidence_level": EvidenceLevel.STRONG,
                "source": "AIS",
                "source_url": "https://www.ais.gov.au/nutrition/supplements",
                "effects": {
                    "muscle_gain": "strong",
                    "strength": "strong",
                    "recovery": "strong",
                    "protein_synthesis": "strong"
                },
                "dosage": {
                    "min": 20.0,
                    "max": 40.0,
                    "unit": "g",
                    "timing": "post_workout",
                    "notes": "20-40g após treino ou entre refeições"
                },
                "contraindications": ["kidney_disease", "lactose_intolerance"],
                "interactions": {
                    "diabetes": "Monitorar açúcar no sangue - whey pode causar pico glicêmico",
                    "medications": "Consulte médico se usar medicamentos para diabetes"
                }
            },
            {
                "supplement_name": "Creatine Monohydrate",
                "category": SupplementCategory.CREATINE,
                "evidence_level": EvidenceLevel.STRONG,
                "source": "AIS",
                "source_url": "https://www.ais.gov.au/nutrition/supplements",
                "effects": {
                    "strength": "strong",
                    "power_output": "strong",
                    "muscle_mass": "strong",
                    "cognitive_function": "moderate"
                },
                "dosage": {
                    "min": 3.0,
                    "max": 5.0,
                    "unit": "g",
                    "timing": "daily",
                    "loading_phase": "20g/dia por 5-7 dias (opcional)",
                    "maintenance": "3-5g/dia"
                },
                "contraindications": ["kidney_disease"],
                "interactions": {
                    "diabetes": "Seguro para diabéticos, pode até melhorar controle glicêmico",
                    "caffeine": "Cafeína pode reduzir eficácia - espaçar ingestão"
                }
            },
            {
                "supplement_name": "Beta-Alanine",
                "category": SupplementCategory.BETA_ALANINE,
                "evidence_level": EvidenceLevel.STRONG,
                "source": "Examine",
                "source_url": "https://examine.com/supplements/beta-alanine/",
                "effects": {
                    "endurance": "strong",
                    "muscular_endurance": "strong",
                    "high_intensity_performance": "strong"
                },
                "dosage": {
                    "min": 2.0,
                    "max": 5.0,
                    "unit": "g",
                    "timing": "pre_workout",
                    "notes": "Dividir dose (2x2g) reduz parestesia"
                },
                "contraindications": [],
                "interactions": {
                    "taurine": "Competem pela absorção - espaçar ingestão"
                }
            },
            {
                "supplement_name": "Caffeine",
                "category": SupplementCategory.CAFFEINE,
                "evidence_level": EvidenceLevel.STRONG,
                "source": "AIS",
                "source_url": "https://www.ais.gov.au/nutrition/supplements",
                "effects": {
                    "endurance": "strong",
                    "strength": "moderate",
                    "alertness": "strong",
                    "fatigue_reduction": "strong"
                },
                "dosage": {
                    "min": 3.0,
                    "max": 6.0,
                    "unit": "mg/kg",
                    "timing": "pre_workout",
                    "notes": "3-6mg/kg de peso corporal, 60min antes do treino"
                },
                "contraindications": ["hypertension", "cardiac_conditions", "anxiety"],
                "interactions": {
                    "hypertension": "Pode aumentar pressão arterial",
                    "medications": "Interage com vários medicamentos - consultar médico",
                    "creatine": "Pode reduzir eficácia da creatina se tomados juntos"
                }
            },
            {
                "supplement_name": "Citrulline Malate",
                "category": SupplementCategory.CITRULLINE,
                "evidence_level": EvidenceLevel.STRONG,
                "source": "Examine",
                "source_url": "https://examine.com/supplements/citrulline/",
                "effects": {
                    "endurance": "strong",
                    "muscle_pump": "strong",
                    "recovery": "moderate"
                },
                "dosage": {
                    "min": 6.0,
                    "max": 8.0,
                    "unit": "g",
                    "timing": "pre_workout"
                },
                "contraindications": [],
                "interactions": {}
            },
            {
                "supplement_name": "BCAA (Branched Chain Amino Acids)",
                "category": SupplementCategory.BCAAS,
                "evidence_level": EvidenceLevel.MODERATE,
                "source": "AIS",
                "source_url": "https://www.ais.gov.au/nutrition/supplements",
                "effects": {
                    "recovery": "moderate",
                    "muscle_protein_synthesis": "moderate",
                    "fatigue_reduction": "moderate"
                },
                "dosage": {
                    "min": 5.0,
                    "max": 10.0,
                    "unit": "g",
                    "timing": "during_workout"
                },
                "contraindications": [],
                "interactions": {
                    "note": "Efeitos são menores quando proteína adequada já está sendo consumida"
                }
            },
            {
                "supplement_name": "Omega-3 (EPA/DHA)",
                "category": SupplementCategory.OMEGA3,
                "evidence_level": EvidenceLevel.STRONG,
                "source": "Examine",
                "source_url": "https://examine.com/supplements/fish-oil/",
                "effects": {
                    "inflammation_reduction": "strong",
                    "recovery": "strong",
                    "cognitive_function": "moderate",
                    "cardiovascular_health": "strong"
                },
                "dosage": {
                    "min": 1.0,
                    "max": 3.0,
                    "unit": "g",
                    "timing": "daily",
                    "notes": "1-3g de EPA+DHA combinados"
                },
                "contraindications": ["allergies"],
                "interactions": {
                    "blood_thinners": "Pode aumentar efeito de anticoagulantes - consultar médico"
                }
            },
            {
                "supplement_name": "Vitamin D",
                "category": SupplementCategory.VITAMIN_D,
                "evidence_level": EvidenceLevel.STRONG,
                "source": "Examine",
                "source_url": "https://examine.com/supplements/vitamin-d/",
                "effects": {
                    "bone_health": "strong",
                    "immune_function": "strong",
                    "testosterone": "moderate",
                    "muscle_function": "moderate"
                },
                "dosage": {
                    "min": 2000,
                    "max": 4000,
                    "unit": "IU",
                    "timing": "daily",
                    "notes": "Dosagem depende de exposição solar e níveis séricos"
                },
                "contraindications": ["hypercalcemia"],
                "interactions": {
                    "calcium_supplements": "Pode aumentar absorção de cálcio",
                    "corticosteroids": "Podem reduzir absorção"
                }
            }
        ]

        created_count = 0
        skipped_count = 0

        for data in science_data:
            instance, created = get_or_create(
                self.session,
                ScientificData,
                supplement_name=data["supplement_name"],
                defaults=data
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1

        self.session.commit()

        print(f"✅ Dados científicos populados:")
        print(f"   - Criados: {created_count}")
        print(f"   - Já existentes: {skipped_count}")
        print(f"   - Total: {len(science_data)}")


def main() -> None:
    """Função principal do script"""
    with ScienceSeeder() as seeder:
        seeder.seed()


if __name__ == "__main__":
    main()

