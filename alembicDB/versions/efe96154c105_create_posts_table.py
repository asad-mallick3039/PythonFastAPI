"""create Posts table

Revision ID: efe96154c105
Revises: 
Create Date: 2024-09-04 22:41:12.642506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efe96154c105'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('Posts', sa.Column('id', sa.Integer(), nullable=False, primary_key= True),
                    sa.Column('title', sa.String, nullable= False))
    pass


def downgrade():
    op.drop_table('Posts')
    pass
