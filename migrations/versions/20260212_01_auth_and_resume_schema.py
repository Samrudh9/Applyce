"""add oauth accounts and missing resume_history column

Revision ID: 20260212_01
Revises: 
Create Date: 2026-02-12
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision = '20260212_01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = inspect(bind)

    resume_columns = {c['name'] for c in inspector.get_columns('resume_history')} if 'resume_history' in inspector.get_table_names() else set()
    if 'extracted_text' not in resume_columns:
        with op.batch_alter_table('resume_history', schema=None) as batch_op:
            batch_op.add_column(sa.Column('extracted_text', sa.Text(), nullable=True))

    if 'users' in inspector.get_table_names():
        with op.batch_alter_table('users', schema=None) as batch_op:
            batch_op.alter_column('password_hash', existing_type=sa.String(length=256), nullable=True)

    if 'oauth_accounts' in inspector.get_table_names():
        return

    op.create_table(
        'oauth_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('provider', sa.String(length=50), nullable=False),
        sa.Column('provider_user_id', sa.String(length=255), nullable=False),
        sa.Column('provider_email', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('provider', 'provider_user_id', name='uq_oauth_provider_user')
    )
    op.create_index(op.f('ix_oauth_accounts_user_id'), 'oauth_accounts', ['user_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_oauth_accounts_user_id'), table_name='oauth_accounts')
    op.drop_table('oauth_accounts')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash', existing_type=sa.String(length=256), nullable=False)
    with op.batch_alter_table('resume_history', schema=None) as batch_op:
        batch_op.drop_column('extracted_text')
