"""Create all tables

Revision ID: c74d5d00111c
Revises: 
Create Date: 2025-02-15 17:52:11.713033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c74d5d00111c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('login', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_login'), 'user', ['login'], unique=True)

    op.create_table(
        'receipt',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('payment_type', sa.String(), nullable=False),
        sa.Column('payment_amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('rest', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_receipt_id'), 'receipt', ['id'], unique=False)

    op.create_table(
        'receipt_product',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('receipt_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['receipt_id'], ['receipt.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_receipt_product_id'), 'receipt_product', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_receipt_product_id'), table_name='receipt_product')
    op.drop_table('receipt_product')
    op.drop_index(op.f('ix_receipt_id'), table_name='receipt')
    op.drop_table('receipt')
    op.drop_index(op.f('ix_user_login'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')
