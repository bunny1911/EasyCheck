"""Added values in table for save payment-method

Revision ID: b3137f6be01d
Revises: fe04b4870625
Create Date: 2025-02-14 22:19:07.142810

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b3137f6be01d'
down_revision: Union[str, None] = 'fe04b4870625'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Inserting default payment methods into the 'payment_method' table
    op.execute(
        """
        INSERT INTO payment_method (title, code) VALUES 
            ('Cash', 'CASH'),
            ('Card', 'CARD');
        """
    )


def downgrade():
    # Removing inserted payment methods
    op.execute(
        """
        DELETE FROM payment_method WHERE code IN ('CASH', 'CARD');
        """
    )
