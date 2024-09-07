"""Add Content Attribute to Posts table

Revision ID: c1b4c5387ebf
Revises: efe96154c105
Create Date: 2024-09-04 22:58:37.761032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1b4c5387ebf'
down_revision: Union[str, None] = 'efe96154c105'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('Posts', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade():
    op.drop_column('Posts', 'content')
    pass
