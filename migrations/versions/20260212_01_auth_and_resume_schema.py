"""prepare auth/resume schema foundations

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
    tables = set(inspector.get_table_names())

    if 'users' not in tables:
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('username', sa.String(length=80), nullable=False),
            sa.Column('email', sa.String(length=120), nullable=False),
            sa.Column('password_hash', sa.String(length=256), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('last_login', sa.DateTime(), nullable=True),
            sa.Column('is_active', sa.Boolean(), nullable=True),
            sa.Column('reset_token', sa.String(length=100), nullable=True),
            sa.Column('reset_token_expiry', sa.DateTime(), nullable=True),
            sa.Column('account_type', sa.String(length=20), nullable=True),
            sa.Column('resume_scans_today', sa.Integer(), nullable=True),
            sa.Column('resume_scans_total', sa.Integer(), nullable=True),
            sa.Column('last_scan_date', sa.Date(), nullable=True),
            sa.Column('premium_expires_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('username'),
            sa.UniqueConstraint('email'),
        )
        tables.add('users')

    if 'users' in tables:
        user_columns = {c['name'] for c in inspector.get_columns('users')}
        if 'password_hash' in user_columns:
            with op.batch_alter_table('users', schema=None) as batch_op:
                batch_op.alter_column('password_hash', existing_type=sa.String(length=256), nullable=True)

    if 'resume_history' in tables:
        resume_columns = {c['name'] for c in inspector.get_columns('resume_history')}
        if 'extracted_text' not in resume_columns:
            with op.batch_alter_table('resume_history', schema=None) as batch_op:
                batch_op.add_column(sa.Column('extracted_text', sa.Text(), nullable=True))


def downgrade():
    bind = op.get_bind()
    inspector = inspect(bind)
    tables = set(inspector.get_table_names())

    if 'users' in tables:
        user_columns = {c['name'] for c in inspector.get_columns('users')}
        if 'password_hash' in user_columns:
            # Intentionally do not revert password_hash to non-nullable here.
            # OAuth-only users may have NULL password_hash values, and enforcing
            # a NOT NULL constraint during downgrade could cause a constraint
            # violation. To keep downgrades safe, we leave the column nullable.
            pass
