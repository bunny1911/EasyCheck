"""Create all tables

Revision ID: fe04b4870625
Revises: 
Create Date: 2025-02-14 22:11:45.540065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fe04b4870625'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create table for save payment methods
    op.create_table(
        'payment_method',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('code', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.UniqueConstraint('title')
    )

    # Create table for save users
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
    # Create index for 'user' table for 'id' column
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)

    # Create index for 'user' table for 'login' column
    op.create_index(op.f('ix_user_login'), 'user', ['login'], unique=True)

    # Create table for save receipts
    op.create_table(
        'receipt',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('total', sa.Float(precision=10, asdecimal=2), nullable=False),
        sa.Column('payment_method_id', sa.Integer(), nullable=False),
        sa.Column('payment_amount', sa.Float(precision=10, asdecimal=2), nullable=False),
        sa.Column('rest', sa.Float(precision=10, asdecimal=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['payment_method_id'], ['payment_method.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index for 'receipt' table for 'id' column
    op.create_index(op.f('ix_receipt_id'), 'receipt', ['id'], unique=False)

    # Create table for save receipt items
    op.create_table(
        'receipt_item',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('receipt_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('price', sa.Float(precision=10, asdecimal=2), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['receipt_id'], ['receipt.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create index for 'receipt_item' table for 'id' column
    op.create_index(op.f('ix_receipt_item_id'), 'receipt_item', ['id'], unique=False)


def downgrade() -> None:
    # Drop index for in 'id' column in 'receipt_item' table
    op.drop_index(op.f('ix_receipt_item_id'), table_name='receipt_item')

    # Drop 'receipt_item' table
    op.drop_table('receipt_item')

    # Drop index for in 'id' column in 'receipt' table
    op.drop_index(op.f('ix_receipt_id'), table_name='receipt')

    # Drop 'receipt' table
    op.drop_table('receipt')

    # Drop index for in 'login' column in 'user' table
    op.drop_index(op.f('ix_user_login'), table_name='user')

    # Drop index for in 'id' column in 'user' table
    op.drop_index(op.f('ix_user_id'), table_name='user')

    # Drop 'user' table
    op.drop_table('user')

    # Drop 'payment_method' table
    op.drop_table('payment_method')
