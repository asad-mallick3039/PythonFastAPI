"""Complete Posts table created

Revision ID: 1fad9b21f964
Revises: ac1af48b99ae
Create Date: 2024-09-04 23:43:32.170578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fad9b21f964'
down_revision: Union[str, None] = 'ac1af48b99ae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Posts', sa.Column(
                    'published', sa.Boolean(), nullable=False, server_default= 'TRUE'))
    op.add_column('Posts', sa.Column(
                    'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('Posts', 'published')
    op.drop_column('Posts', 'created_at')
    pass
