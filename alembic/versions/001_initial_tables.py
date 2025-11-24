"""Criar tabelas iniciais (Tenant, ScientificData, UserProfile, Product, InteractionLog)

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Criar extensões PostgreSQL
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
    op.execute("CREATE EXTENSION IF NOT EXISTS \"pg_trgm\";")
    
    # ============================================================================
    # TENANT
    # ============================================================================
    op.create_table(
        'tenants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('plan', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_tenant_name', 'tenants', ['name'], unique=False)
    
    # ============================================================================
    # SCIENTIFIC DATA (GLOBAL)
    # ============================================================================
    op.create_table(
        'scientific_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('supplement_name', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('evidence_level', sa.String(), nullable=False),
        sa.Column('source', sa.String(length=100), nullable=False),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('effects', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('dosage', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('contraindications', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('interactions', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_scientific_supplement', 'scientific_data', ['supplement_name'], unique=False)
    op.create_index('idx_scientific_category', 'scientific_data', ['category'], unique=False)
    op.create_index('idx_scientific_evidence', 'scientific_data', ['evidence_level'], unique=False)
    op.create_index('idx_scientific_source', 'scientific_data', ['source'], unique=False)
    
    # ============================================================================
    # USER PROFILE
    # ============================================================================
    op.create_table(
        'user_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('biometrics', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('goal', sa.String(), nullable=False),
        sa.Column('dietary_restrictions', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('medical_conditions', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('budget_range', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_tenant', 'user_profiles', ['tenant_id'], unique=False)
    op.create_index('idx_user_goal', 'user_profiles', ['goal'], unique=False)
    op.create_index('idx_user_budget', 'user_profiles', ['budget_range'], unique=False)
    op.create_index('idx_user_tenant_goal', 'user_profiles', ['tenant_id', 'goal'], unique=False)
    
    # ============================================================================
    # PRODUCT
    # ============================================================================
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('brand_name', sa.String(length=255), nullable=False),
        sa.Column('product_name', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('nutritional_info', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('certifications', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('stock_quantity', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_product_tenant', 'products', ['tenant_id'], unique=False)
    op.create_index('idx_product_brand', 'products', ['brand_name'], unique=False)
    op.create_index('idx_product_category', 'products', ['category'], unique=False)
    op.create_index('idx_product_tenant_category', 'products', ['tenant_id', 'category'], unique=False)
    op.create_index('idx_product_active', 'products', ['is_active', 'tenant_id'], unique=False)
    op.create_index('idx_product_price', 'products', ['price'], unique=False)
    
    # ============================================================================
    # INTERACTION LOG
    # ============================================================================
    op.create_table(
        'interaction_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('user_profile_id', sa.Integer(), nullable=True),
        sa.Column('session_id', sa.String(length=255), nullable=False),
        sa.Column('query_text', sa.Text(), nullable=True),
        sa.Column('recommended_products', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('ranking_data', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('selected_product_id', sa.Integer(), nullable=True),
        sa.Column('user_feedback', sa.Text(), nullable=True),
        sa.Column('satisfaction_score', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('ip_address', sa.String(length=45), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.ForeignKeyConstraint(['user_profile_id'], ['user_profiles.id'], ),
        sa.ForeignKeyConstraint(['selected_product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_log_tenant', 'interaction_logs', ['tenant_id'], unique=False)
    op.create_index('idx_log_created', 'interaction_logs', ['created_at'], unique=False)
    op.create_index('idx_log_tenant_created', 'interaction_logs', ['tenant_id', 'created_at'], unique=False)
    op.create_index('idx_log_selected', 'interaction_logs', ['selected_product_id'], unique=False)
    op.create_index('idx_log_session', 'interaction_logs', ['session_id'], unique=False)


def downgrade() -> None:
    # Remover tabelas na ordem inversa (respeitando foreign keys)
    op.drop_table('interaction_logs')
    op.drop_table('products')
    op.drop_table('user_profiles')
    op.drop_table('scientific_data')
    op.drop_table('tenants')
    
    # Remover extensões (opcional - comentado para não quebrar outros projetos)
    # op.execute("DROP EXTENSION IF EXISTS \"pg_trgm\";")
    # op.execute("DROP EXTENSION IF EXISTS \"uuid-ossp\";")

